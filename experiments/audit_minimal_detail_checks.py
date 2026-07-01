from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "output" / "minimal-detail-audit-2026-06-26"
BASE_URL = "http://127.0.0.1:4174/experiments"

VARIANTS = ["minimal-mono-focus", "minimal-modern-blue", "minimal-warm-editorial"]
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
EXPECTED_GLASS = {"hero.webp", "about.webp", "contact.webp", "taixi.webp", "yanxin.webp", "mengli.webp"}


def inspect_page(page) -> dict:
    return page.evaluate(
        """() => {
          const doc = document.documentElement;
          const body = document.body;
          const viewportWidth = window.innerWidth;
          const scrollWidth = Math.max(doc.scrollWidth, body.scrollWidth);
          const textSelectors = [
            'h1','h2','h3','p','a','button','span','strong','small','dt','dd','li'
          ];
          const textOverflow = Array.from(document.querySelectorAll(textSelectors.join(',')))
            .filter((el) => {
              if (el.closest('.sr-only')) return false;
              const text = (el.textContent || '').trim();
              if (!text || text.length < 2) return false;
              const r = el.getBoundingClientRect();
              if (r.width <= 0 || r.height <= 0) return false;
              const cs = getComputedStyle(el);
              if (cs.position === 'fixed') return false;
              const tooWide = el.scrollWidth > el.clientWidth + 2 && cs.whiteSpace !== 'normal';
              const offscreen = r.left < -2 || r.right > viewportWidth + 2;
              return tooWide || offscreen;
            })
            .slice(0, 20)
            .map((el) => {
              const r = el.getBoundingClientRect();
              return {
                tag: el.tagName.toLowerCase(),
                cls: String(el.className || '').slice(0, 80),
                text: (el.textContent || '').trim().slice(0, 80),
                left: Math.round(r.left),
                right: Math.round(r.right),
                clientWidth: el.clientWidth,
                scrollWidth: el.scrollWidth
              };
            });
          const brokenImages = Array.from(document.images)
            .filter((img) => !img.complete || img.naturalWidth === 0)
            .map((img) => img.getAttribute('src') || '');
          const internalLinks = Array.from(document.querySelectorAll('a[href]'))
            .map((a) => a.getAttribute('href') || '')
            .filter((href) => href && !href.startsWith('mailto:') && !href.startsWith('tel:') && !href.startsWith('#'));
          return {
            title: document.title,
            overflow: scrollWidth - viewportWidth,
            brokenImages,
            textOverflow,
            internalLinks,
            h1: document.querySelector('h1')?.textContent?.trim() || ''
          };
        }"""
    )


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    asset_checks = []
    for variant in VARIANTS:
        glass_dir = ROOT / "experiments" / variant / "assets" / "glass"
        files = {p.name for p in glass_dir.glob("*.webp")}
        image_sizes = {}
        for image_path in sorted(glass_dir.glob("*.webp")):
            with Image.open(image_path) as image:
                image_sizes[image_path.name] = {"width": image.width, "height": image.height, "bytes": image_path.stat().st_size}
        asset_checks.append(
            {
                "variant": variant,
                "missing": sorted(EXPECTED_GLASS - files),
                "extra": sorted(files - EXPECTED_GLASS),
                "images": image_sizes,
            }
        )

    rows = []
    link_failures = []
    browser_messages: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(device_scale_factor=1)
        page = context.new_page()
        page.on("console", lambda msg: browser_messages.append({"type": "console", "level": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: browser_messages.append({"type": "pageerror", "text": str(exc)}))
        page.on("requestfailed", lambda request: browser_messages.append({"type": "requestfailed", "url": request.url, "failure": request.failure}))
        page.on("response", lambda response: browser_messages.append({"type": "http", "url": response.url, "status": response.status}) if response.status >= 400 else None)

        checked_links = set()
        for variant in VARIANTS:
            for page_name, route in PAGES:
                url = f"{BASE_URL}/{variant}/{route}"
                for viewport_name, width, height in VIEWPORTS:
                    page.set_viewport_size({"width": width, "height": height})
                    page.goto(url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(120)
                    audit = inspect_page(page)
                    rows.append({"variant": variant, "page": page_name, "viewport": viewport_name, "audit": audit})
                    if viewport_name == "desktop":
                        for href in audit["internalLinks"]:
                            target = page.evaluate(
                                """(href) => new URL(href, location.href).href""",
                                href,
                            )
                            if target in checked_links:
                                continue
                            checked_links.add(target)
                            response = page.goto(target, wait_until="load", timeout=20000)
                            status = response.status if response else 0
                            if status >= 400 or status == 0:
                                link_failures.append({"from": url, "href": href, "target": target, "status": status})
                            page.goto(url, wait_until="load", timeout=20000)

        context.close()
        browser.close()

    issues = [
        row
        for row in rows
        if row["audit"]["overflow"] > 0 or row["audit"]["brokenImages"] or row["audit"]["textOverflow"]
    ]
    warnings = [
        msg
        for msg in browser_messages
        if msg.get("type") in {"pageerror", "requestfailed", "http"} or msg.get("level") in {"warning", "warn", "error"}
    ]
    summary = {
        "pageChecks": len(rows),
        "assetChecks": asset_checks,
        "issues": issues,
        "linkFailures": link_failures,
        "warnings": warnings,
    }
    (OUT_ROOT / "detail-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
