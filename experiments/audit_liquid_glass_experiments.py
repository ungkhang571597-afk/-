from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "output" / "liquid-glass-audit-2026-06-26"
BASE_URL = "http://127.0.0.1:4174/experiments"

VARIANTS = ["liquid-glass-v1", "liquid-glass-v2", "liquid-glass-v3", "liquid-glass-final"]
PAGES = [
    ("home", "index.html"),
    ("about", "about.html"),
    ("yanxin", "cases/yanxin.html"),
    ("mengli", "cases/mengli.html"),
    ("contact", "contact.html"),
]
VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet", 900, 1100),
    ("mobile", 390, 844),
    ("narrow", 360, 780),
]
POSITIONS = ["top", "mid", "bottom"]


def browser_audit(page) -> dict:
    return page.evaluate(
        """() => {
          const doc = document.documentElement;
          const body = document.body;
          const viewportWidth = window.innerWidth;
          const scrollWidth = Math.max(doc.scrollWidth, body.scrollWidth);
          const overflow = scrollWidth - viewportWidth;
          const brokenImages = Array.from(document.images)
            .filter((img) => !img.complete || img.naturalWidth === 0)
            .map((img) => img.getAttribute("src") || "");
          const offenders = Array.from(document.querySelectorAll("body *"))
            .map((el) => {
              const r = el.getBoundingClientRect();
              const cs = getComputedStyle(el);
              return {
                tag: el.tagName.toLowerCase(),
                cls: (el.className && String(el.className).slice(0, 120)) || "",
                left: Math.round(r.left),
                right: Math.round(r.right),
                width: Math.round(r.width),
                position: cs.position
              };
            })
            .filter((r) => r.width > 0 && r.position !== "fixed" && (r.left < -3 || r.right > viewportWidth + 3))
            .slice(0, 12);
          const fontBody = getComputedStyle(body).fontFamily;
          const h1 = document.querySelector("h1");
          const fontH1 = h1 ? getComputedStyle(h1).fontFamily + " / " + getComputedStyle(h1).fontWeight : "";
          const bgResources = performance.getEntriesByType("resource")
            .map((entry) => entry.name)
            .filter((name) => /assets\\/glass|wechat-qr|font-faces|\\.ttf|\\.webp|\\.jpg|\\.png/.test(name));
          return {
            title: document.title,
            viewportWidth,
            scrollWidth,
            overflow,
            brokenImages,
            offenders,
            height: Math.max(doc.scrollHeight, body.scrollHeight),
            fontBody,
            fontH1,
            bgResources
          };
        }"""
    )


def save_contact_sheet(variant_dir: Path, variant: str) -> Path:
    shots = sorted(variant_dir.glob("*.png"))
    thumb_w, thumb_h = 220, 138
    pad = 14
    cols = 5
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (thumb_h + 46 + pad) + pad), "#efe7db")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    except Exception:
        font = ImageFont.load_default()
    for index, shot in enumerate(shots):
        img = Image.open(shot).convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
        x = pad + (index % cols) * (thumb_w + pad)
        y = pad + (index // cols) * (thumb_h + 46 + pad)
        frame = Image.new("RGB", (thumb_w, thumb_h), "#11100e")
        frame.paste(img, ((thumb_w - img.width) // 2, (thumb_h - img.height) // 2))
        sheet.paste(frame, (x, y))
        label = shot.stem.replace("__", " / ")
        draw.text((x, y + thumb_h + 7), label[:31], fill="#221915", font=font)
    out = OUT_ROOT / f"contact-sheet-{variant}.jpg"
    sheet.save(out, quality=90)
    return out


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    audit_rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(device_scale_factor=1)
        page = context.new_page()
        browser_messages: list[dict] = []

        page.on("console", lambda msg: browser_messages.append({"type": "console", "level": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: browser_messages.append({"type": "pageerror", "text": str(exc)}))
        page.on("requestfailed", lambda request: browser_messages.append({"type": "requestfailed", "url": request.url, "failure": request.failure}))
        page.on("response", lambda response: browser_messages.append({"type": "http", "url": response.url, "status": response.status}) if response.status >= 400 else None)

        for variant in VARIANTS:
            variant_dir = OUT_ROOT / variant
            variant_dir.mkdir(parents=True, exist_ok=True)
            for page_name, route in PAGES:
                url = f"{BASE_URL}/{variant}/{route}"
                for viewport_name, width, height in VIEWPORTS:
                    page.set_viewport_size({"width": width, "height": height})
                    page.goto(url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(180)
                    audit = browser_audit(page)
                    audit_rows.append({"variant": variant, "page": page_name, "viewport": viewport_name, "audit": audit})
                    max_scroll = page.evaluate("() => Math.max(0, document.documentElement.scrollHeight - window.innerHeight)")
                    for position in POSITIONS:
                        if position == "top":
                            y = 0
                        elif position == "mid":
                            y = round(max_scroll / 2)
                        else:
                            y = max_scroll
                        page.evaluate("(y) => window.scrollTo(0, y)", y)
                        page.wait_for_timeout(110)
                        page.screenshot(path=variant_dir / f"{page_name}__{viewport_name}-{position}.png", full_page=False)
                page.set_viewport_size({"width": 390, "height": 844})
                page.goto(url, wait_until="load", timeout=20000)
                page.wait_for_timeout(160)
                button = page.locator(".menu-toggle")
                if button.count() == 1:
                    button.click()
                    page.wait_for_timeout(160)
                    page.screenshot(path=variant_dir / f"{page_name}__mobile-menu.png", full_page=False)

            save_contact_sheet(variant_dir, variant)

        context.close()
        browser.close()

    issues = [
        row
        for row in audit_rows
        if row["audit"]["overflow"] > 0 or row["audit"]["brokenImages"] or row["audit"]["offenders"]
    ]
    warnings = [
        msg
        for msg in browser_messages
        if msg.get("type") in {"pageerror", "requestfailed", "http"} or msg.get("level") in {"warning", "warn", "error"}
    ]
    summary = {
        "screenshots": sum(len(list((OUT_ROOT / variant).glob("*.png"))) for variant in VARIANTS),
        "contactSheets": [str(p) for p in sorted(OUT_ROOT.glob("contact-sheet-*.jpg"))],
        "issues": issues,
        "warnings": warnings,
    }
    (OUT_ROOT / "audit-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
