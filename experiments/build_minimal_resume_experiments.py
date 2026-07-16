from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

from build_liquid_glass_experiments import (
    CASE_DATA,
    EXPERIMENTS,
    PERSON_LD,
    ROOT,
    SITE_JS,
    about_main,
    case_main,
    contact_main,
    ensure_clean_dir,
    home_main,
    page,
    save_webp,
)


GENERATED = Path(r"C:\Users\ZHONGTAO\.codex\generated_images\019eff09-c49c-7610-b21f-8b467bae58eb")
SOURCE_ASSETS = EXPERIMENTS / "source-assets"

THEMES = {
    "mono": {
        "folder": "minimal-mono-focus",
        "label": "Mono Focus",
        "body": "minimal-mono",
    },
    "blue": {
        "folder": "minimal-modern-blue",
        "label": "Modern Blue Clean",
        "body": "minimal-blue",
    },
    "warm": {
        "folder": "minimal-warm-editorial",
        "label": "Warm Editorial Grid",
        "body": "minimal-warm",
    },
}

ASSET_SOURCES = {
    "mono": {
        "hero": GENERATED / "ig_060bf69d73716a39016a3e0cd9d2ec8196a47cb9702a28fc75.png",
        "about": GENERATED / "ig_060bf69d73716a39016a3e0d1813648196a44575648e6dd5cf.png",
        "contact": GENERATED / "ig_060bf69d73716a39016a3e0d4e6fa08196af2e08e1765f1360.png",
        "taixi": SOURCE_ASSETS / "taixi-mono-gpt2.png",
        "yanxin": GENERATED / "ig_060bf69d73716a39016a3e0dc2ab148196995e4b610f43e654.png",
        "mengli": GENERATED / "ig_060bf69d73716a39016a3e0e048fd081968bdafbc482b44164.png",
    },
    "blue": {
        "hero": GENERATED / "ig_060bf69d73716a39016a3e0e42811c8196930bba218db6d068.png",
        "about": GENERATED / "ig_060bf69d73716a39016a3e0e8419e08196b556594b8b5eeefa.png",
        "contact": GENERATED / "ig_060bf69d73716a39016a3e0eca5d988196a59a728bd2e71674.png",
        "taixi": SOURCE_ASSETS / "taixi-blue-gpt2.png",
        "yanxin": GENERATED / "ig_060bf69d73716a39016a3e0f5cc12481968406cf086ca63d95.png",
        "mengli": GENERATED / "ig_060bf69d73716a39016a3e0f999c288196a8cc4b3b912b4afe.png",
    },
    "warm": {
        "hero": GENERATED / "ig_060bf69d73716a39016a3e0fe186688196a226bd55bc9be976.png",
        "about": GENERATED / "ig_060bf69d73716a39016a3e1025859c8196be21afb836164496.png",
        "contact": GENERATED / "ig_060bf69d73716a39016a3e106d162481968a72b2985e900e71.png",
        "taixi": SOURCE_ASSETS / "taixi-warm-gpt2.png",
        "yanxin": GENERATED / "ig_060bf69d73716a39016a3e110a4b408196934501523cb03184.png",
        "mengli": GENERATED / "ig_060bf69d73716a39016a3e1157ac4481968ad602867ead3955.png",
    },
}

ASSET_CROPS = {
    ("blue", "mengli"): (0.29, 0.07, 0.96, 0.9),
}


def copy_base_assets(site_dir: Path) -> None:
    (site_dir / "assets" / "brand").mkdir(parents=True, exist_ok=True)
    (site_dir / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    for font in (ROOT / "assets" / "fonts").iterdir():
        shutil.copy2(font, site_dir / "assets" / "fonts" / font.name)
    for filename in ["favicon.svg"]:
        src = ROOT / filename
        if src.exists():
            shutil.copy2(src, site_dir / filename)
    shutil.copy2(
        ROOT / "assets" / "brand" / "wechat-qr-mono.png",
        site_dir / "assets" / "brand" / "wechat-qr-mono.png",
    )
    shutil.copy2(
        ROOT / "assets" / "brand" / "og-cover.jpg",
        site_dir / "assets" / "brand" / "og-cover.jpg",
    )
    for filename in ["portrait-zt-square.webp", "portrait-zt-vertical.webp", "portrait-zt-card.webp"]:
        shutil.copy2(
            ROOT / "assets" / "brand" / filename,
            site_dir / "assets" / "brand" / filename,
        )


def save_visual_webp(
    src: Path,
    dest: Path,
    crop: tuple[float, float, float, float] | None = None,
    max_size: tuple[int, int] = (1900, 1188),
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as image:
        image = image.convert("RGB")
        if crop:
            width, height = image.size
            left, top, right, bottom = crop
            image = image.crop((
                round(width * left),
                round(height * top),
                round(width * right),
                round(height * bottom),
            ))
        image.thumbnail(max_size, Image.LANCZOS)
        image.save(dest, "WEBP", quality=84, method=6)


def prepare_visuals(site_dir: Path, theme_key: str) -> None:
    glass_dir = site_dir / "assets" / "glass"
    for key, source in ASSET_SOURCES[theme_key].items():
        save_visual_webp(source, glass_dir / f"{key}.webp", ASSET_CROPS.get((theme_key, key)))


def css_for() -> str:
    return r'''@import url("assets/fonts/font-faces.css");

:root {
  --font-display: "Noto Serif SC", "Songti SC", "STSong", "SimSun", Georgia, serif;
  --font-body: "Noto Sans SC", "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
  --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
  --site-width: 1180px;
  --header-height: 72px;
  --radius: 6px;
  --ease: cubic-bezier(.2, .75, .2, 1);
}

body.minimal-mono {
  --bg: #f4f0e7;
  --paper: #fbf8f1;
  --paper-strong: #fffdf8;
  --text: #171717;
  --muted: #5f5f5b;
  --soft: #8b8a84;
  --line: 31, 31, 29;
  --line-alpha: .14;
  --accent: #171717;
  --accent-soft: #d7d3cb;
  --accent-ink: #ffffff;
  --shadow: 22, 22, 20;
  --image-opacity: .2;
}

body.minimal-blue {
  --bg: #eef5fb;
  --paper: #fbfdff;
  --paper-strong: #ffffff;
  --text: #17263a;
  --muted: #607084;
  --soft: #8fa1b8;
  --line: 35, 74, 112;
  --line-alpha: .15;
  --accent: #1e5389;
  --accent-soft: #dbe8f4;
  --accent-ink: #ffffff;
  --shadow: 38, 75, 112;
  --image-opacity: .22;
}

body.minimal-warm {
  --bg: #f6eddf;
  --paper: #fffaf1;
  --paper-strong: #fffdf8;
  --text: #251b16;
  --muted: #715f53;
  --soft: #9b8472;
  --line: 93, 49, 39;
  --line-alpha: .15;
  --accent: #7b1c1f;
  --accent-soft: #eadac8;
  --accent-ink: #fff8ee;
  --shadow: 94, 70, 48;
  --image-opacity: .18;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  overflow-x: clip;
}

[id] {
  scroll-margin-top: calc(var(--header-height) + 28px);
}

body {
  margin: 0;
  min-height: 100vh;
  overflow-x: clip;
  color: var(--text);
  font-family: var(--font-body);
  line-height: 1.72;
  background:
    linear-gradient(90deg, rgba(var(--line), .045) 0 1px, transparent 1px) 0 0 / 72px 72px,
    linear-gradient(0deg, rgba(var(--line), .032) 0 1px, transparent 1px) 0 0 / 72px 72px,
    var(--bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  pointer-events: none;
  opacity: .5;
  background:
    radial-gradient(circle at 14% 12%, rgba(var(--line), .08), transparent 28%),
    radial-gradient(circle at 86% 18%, rgba(var(--line), .05), transparent 24%),
    repeating-linear-gradient(90deg, rgba(var(--line), .035) 0 1px, transparent 1px 8px);
}

body.nav-open {
  overflow: hidden;
}

body,
h1,
h2,
h3,
p,
ul,
ol,
dl,
dd {
  margin: 0;
}

ul,
ol {
  padding: 0;
}

li {
  list-style: none;
}

img {
  display: block;
  max-width: 100%;
  height: auto;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
textarea {
  font: inherit;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.shell {
  width: min(100% - 64px, var(--site-width));
  margin: 0 auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  min-height: var(--header-height);
  border-bottom: 1px solid rgba(var(--line), .12);
  background: color-mix(in srgb, var(--paper) 88%, transparent);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.header-inner {
  min-height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 26px;
}

.brand {
  display: inline-grid;
  grid-template-columns: 44px minmax(0, auto);
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.brand-mark {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(var(--line), .22);
  border-radius: 2px;
  color: var(--accent-ink);
  background: var(--accent);
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0;
}

.brand-copy {
  display: grid;
  line-height: 1.15;
}

.brand-copy strong {
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 500;
}

.brand-copy small {
  margin-top: 3px;
  color: var(--muted);
  font-size: 12px;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 14px;
}

.site-nav a {
  position: relative;
  padding: 10px 12px;
  border-radius: 4px;
  transition: color .2s ease, background .2s ease;
}

.site-nav a:hover,
.site-nav a:focus-visible,
.site-nav a.is-current {
  color: var(--text);
  background: rgba(var(--line), .055);
  outline: none;
}

.menu-toggle {
  width: 42px;
  height: 42px;
  display: none;
  place-items: center;
  gap: 4px;
  padding: 0;
  border: 1px solid rgba(var(--line), .18);
  border-radius: 4px;
  color: var(--text);
  background: var(--paper-strong);
  cursor: pointer;
}

.menu-toggle span:not(.sr-only) {
  width: 18px;
  height: 1px;
  background: currentColor;
}

.hero,
.page-hero,
.case-hero {
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - var(--header-height));
  padding: 86px 0;
  display: grid;
  align-items: center;
  border-bottom: 1px solid rgba(var(--line), .12);
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: -1;
  background:
    linear-gradient(90deg, var(--bg) 0%, color-mix(in srgb, var(--bg) 88%, transparent) 38%, rgba(255, 255, 255, .42) 72%, rgba(255, 255, 255, .08) 100%),
    var(--page-image, url("assets/glass/hero.webp")) right center / cover no-repeat;
}

.hero-bg::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, transparent 0%, var(--bg) 100%),
    linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, .2) 100%);
  opacity: .54;
}

.home-hero {
  --page-image: url("assets/glass/hero.webp");
}

.about-hero {
  --page-image: url("assets/glass/about.webp");
}

.contact-hero {
  --page-image: url("assets/glass/contact.webp");
}

.case-yanxin-page .case-hero {
  --page-image: url("assets/glass/yanxin.webp");
}

.case-mengli-page .case-hero {
  --page-image: url("assets/glass/mengli.webp");
}

.hero-grid,
.page-hero-grid,
.contact-grid,
.case-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, .92fr) minmax(280px, .42fr);
  align-items: end;
  gap: 54px;
}

.page-hero-grid,
.case-hero-grid,
.contact-grid {
  align-items: center;
}

.hero-copy,
.page-copy,
.case-intro {
  position: relative;
  max-width: 760px;
}

.hero-copy::before,
.page-copy::before,
.case-intro::before {
  content: "";
  display: block;
  width: min(62vw, 520px);
  height: 1px;
  margin-bottom: 28px;
  background: linear-gradient(90deg, var(--accent), rgba(var(--line), .08));
}

.eyebrow,
.breadcrumbs,
.case-tag {
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.45;
  letter-spacing: 0;
  text-transform: uppercase;
}

.breadcrumbs {
  margin-bottom: 20px;
}

h1,
h2,
h3 {
  font-family: var(--font-display);
  font-weight: 500;
  line-height: 1.12;
  letter-spacing: 0;
}

h1 {
  margin-top: 12px;
  font-size: clamp(74px, 10.4vw, 150px);
}

.page-copy h1,
.case-intro h1 {
  font-size: clamp(46px, 7.2vw, 94px);
}

.hero-line,
.page-subtitle {
  margin-top: 18px;
  color: var(--text);
  font-family: var(--font-body);
  font-size: clamp(27px, 3.3vw, 44px);
  font-weight: 500;
  line-height: 1.24;
  text-wrap: balance;
}

.hero-summary,
.page-copy > p:not(.breadcrumbs):not(.eyebrow):not(.page-subtitle),
.case-intro > p:not(.breadcrumbs):not(.page-subtitle) {
  max-width: 680px;
  margin-top: 24px;
  color: var(--muted);
  font-size: 18px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 34px;
}

.btn,
.text-link,
.copy-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.2;
  transition: transform .2s var(--ease), border-color .2s ease, background .2s ease, color .2s ease;
}

.btn {
  padding: 11px 16px;
  border: 1px solid rgba(var(--line), .18);
}

.btn:hover,
.text-link:hover,
.copy-chip:hover {
  transform: translateY(-1px);
}

.btn-primary {
  color: var(--accent-ink);
  border-color: var(--accent);
  background: var(--accent);
}

.btn-ghost {
  color: var(--text);
  background: color-mix(in srgb, var(--paper) 78%, transparent);
}

.text-link {
  color: var(--accent);
  justify-self: end;
}

.glass-panel,
.glass-card {
  position: relative;
  border: 1px solid rgba(var(--line), var(--line-alpha));
  border-radius: var(--radius);
  background: color-mix(in srgb, var(--paper) 91%, transparent);
  box-shadow: 0 22px 50px rgba(var(--shadow), .08);
}

.glass-panel::before,
.glass-card::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background:
    linear-gradient(90deg, rgba(var(--line), .06) 0 1px, transparent 1px) 0 0 / 24px 24px,
    linear-gradient(0deg, rgba(var(--line), .035) 0 1px, transparent 1px) 0 0 / 24px 24px;
  opacity: .36;
}

.hero-panel,
.status-panel,
.qr-panel,
.result-panel,
.summary-panel,
.method-aside,
.trust-panel,
.talk-panel {
  padding: 26px;
}

.panel-portrait,
.identity-chip {
  position: relative;
  z-index: 1;
  display: inline-grid;
  grid-template-columns: 88px minmax(0, 1fr);
  align-items: center;
  gap: 14px;
  max-width: 100%;
  margin: 18px 0 4px;
  padding: 7px 14px 7px 7px;
  border: 1px solid rgba(var(--line), .16);
  border-radius: 4px;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--paper-strong) 92%, transparent), color-mix(in srgb, var(--paper) 80%, transparent)),
    var(--paper);
  box-shadow: 0 18px 36px rgba(var(--shadow), .06);
}

.panel-portrait img,
.identity-chip img {
  width: 88px;
  height: 88px;
  object-fit: cover;
  object-position: center 40%;
  border-radius: 3px;
  filter: saturate(.94) contrast(1.02);
}

.panel-portrait figcaption,
.identity-chip div {
  display: grid;
  gap: 2px;
  min-width: 0;
}

.panel-portrait span,
.identity-chip strong {
  color: var(--text);
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.2;
}

.panel-portrait small,
.identity-chip span {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}

.panel-portrait.compact,
.qr-panel .panel-portrait {
  grid-template-columns: 68px minmax(0, 1fr);
  margin: 18px auto 16px;
  text-align: left;
}

.panel-portrait.compact img,
.qr-panel .panel-portrait img {
  width: 68px;
  height: 68px;
}

.case-author-chip {
  margin: 18px 0 0;
  grid-template-columns: 46px minmax(0, 1fr);
  padding: 6px 13px 6px 6px;
}

.case-author-chip img {
  width: 46px;
  height: 46px;
}

.metric-stack {
  display: grid;
  gap: 0;
  margin-top: 18px;
}

.metric-stack > div,
.metric-stack > article {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  align-items: start;
  padding: 18px 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.metric-stack strong {
  display: block;
  color: var(--accent);
  font-family: var(--font-display);
  font-size: clamp(34px, 4.4vw, 52px);
  font-weight: 500;
  line-height: 1;
  white-space: nowrap;
}

.metric-stack span {
  display: block;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.45;
}

.section {
  padding: 92px 0;
}

.section + .section {
  border-top: 1px solid rgba(var(--line), .08);
}

.section-head {
  display: grid;
  grid-template-columns: minmax(0, .82fr) auto;
  align-items: end;
  gap: 30px;
  margin-bottom: 34px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(var(--line), .13);
}

.section-head h2,
.section-copy h2,
.teaser-panel h2,
.talk-panel h2,
.trust-panel h2,
.method-aside h2,
.result-panel h2,
.summary-panel h2,
.case-text h2 {
  font-size: clamp(30px, 4vw, 54px);
}

.case-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.case-card {
  position: relative;
  min-height: 548px;
  display: grid;
  grid-template-rows: 230px 1fr;
  overflow: hidden;
}

.card-hit {
  position: absolute;
  inset: 0;
  z-index: 4;
}

.case-card:first-child {
  grid-row: auto;
  grid-template-rows: 230px 1fr;
}

.case-media {
  position: relative;
  background: var(--case-image) center / cover no-repeat;
  filter: saturate(.92) contrast(.98);
  border-bottom: 1px solid rgba(var(--line), .12);
}

.case-media::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, color-mix(in srgb, var(--paper) 70%, transparent) 100%);
  opacity: .22;
}

.case-taixi .case-media {
  --case-image: url("assets/glass/taixi.webp");
  background-color: color-mix(in srgb, var(--paper-strong) 82%, var(--accent-soft));
  background-size: contain;
}

.case-yanxin .case-media {
  --case-image: url("assets/glass/yanxin.webp");
}

.case-mengli .case-media {
  --case-image: url("assets/glass/mengli.webp");
}

.case-body {
  position: relative;
  display: grid;
  gap: 16px;
  align-content: start;
  padding: 24px;
}

.case-body h3 {
  font-family: var(--font-body);
  font-size: clamp(29px, 2.1vw, 31px);
  font-weight: 600;
  line-height: 1.18;
  text-wrap: balance;
}

.case-body p,
.section-copy p,
.compact-list p,
.contact-teaser p,
.case-text p,
.case-takeaway span,
.summary-panel dd,
.qr-panel p {
  color: var(--muted);
  font-size: 15px;
  word-break: normal;
  overflow-wrap: break-word;
}

.case-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  margin-top: 2px;
  border-top: 1px solid rgba(var(--line), .12);
}

.case-metrics div {
  padding: 14px 12px 0 0;
  min-width: 0;
}

.case-metrics strong {
  display: block;
  color: var(--accent);
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 500;
  line-height: 1;
  white-space: nowrap;
}

.case-metrics span {
  display: block;
  margin-top: 8px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.35;
}

.method-grid,
.about-grid,
.lower-grid,
.content-grid {
  display: grid;
  grid-template-columns: minmax(0, .88fr) minmax(280px, .42fr);
  gap: 34px;
  align-items: start;
}

.section-copy {
  max-width: 650px;
}

.section-copy p {
  margin-top: 18px;
  font-size: 17px;
}

.method-list,
.compact-list {
  display: grid;
  gap: 0;
}

.method-list {
  padding: 8px 24px;
}

.method-list article,
.compact-list article {
  display: grid;
  grid-template-columns: 54px minmax(0, 1fr);
  gap: 16px;
  padding: 18px 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.method-list article > strong,
.method-list article > p {
  grid-column: 2;
}

.compact-list article {
  grid-template-columns: 1fr;
}

.method-list span {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 12px;
}

.method-list strong,
.compact-list strong,
.case-takeaway strong,
.summary-panel dt {
  font-weight: 600;
}

.teaser-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 30px;
  background:
    linear-gradient(90deg, color-mix(in srgb, var(--paper-strong) 94%, transparent), color-mix(in srgb, var(--accent-soft) 26%, var(--paper)));
}

.teaser-panel p {
  margin-top: 10px;
}

.status-panel strong,
.status-panel span {
  display: block;
}

.status-panel strong + span {
  margin-top: 8px;
  color: var(--muted);
}

.status-panel hr {
  margin: 22px 0;
  border: 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.timeline-panel {
  padding: 22px 28px;
}

.story-timeline {
  position: relative;
  display: grid;
}

.story-timeline > li {
  position: relative;
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 18px;
  padding: 24px 0;
}

.story-timeline > li::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  width: 1px;
  background: rgba(var(--line), .12);
}

.story-timeline > li > span {
  position: relative;
  z-index: 1;
  width: 10px;
  height: 10px;
  margin-top: 11px;
  justify-self: center;
  border: 1px solid var(--accent);
  border-radius: 50%;
  background: var(--paper);
}

.story-timeline > li.is-current > span {
  background: var(--accent);
}

.story-timeline h2 {
  font-family: var(--font-body);
  font-size: 28px;
  font-weight: 600;
  line-height: 1.22;
}

.story-timeline p {
  margin-top: 8px;
  color: var(--muted);
}

.proof-list {
  display: grid;
  gap: 8px;
  margin-top: 14px;
  color: var(--muted);
}

.proof-list li {
  position: relative;
  display: block;
  width: 100%;
  padding-left: 16px;
  line-height: inherit;
}

.proof-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: .82em;
  width: 6px;
  height: 1px;
  background: var(--accent);
}

.case-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}

.case-meta span,
.case-tag {
  display: inline-flex;
  width: fit-content;
  min-height: 28px;
  align-items: center;
  padding: 4px 8px;
  border: 1px solid rgba(var(--line), .13);
  border-radius: 3px;
  color: var(--muted);
  background: color-mix(in srgb, var(--paper) 74%, transparent);
}

.case-takeaway {
  display: grid;
  gap: 0;
  margin-top: 28px;
  padding: 8px 20px;
}

.case-takeaway article {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  gap: 16px;
  padding: 14px 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.case-content {
  padding-top: 72px;
}

.content-grid > *,
.case-text,
.summary-panel {
  min-width: 0;
  max-width: 100%;
}

.case-text {
  padding: 32px;
}

.case-text section + section {
  margin-top: 34px;
  padding-top: 30px;
  border-top: 1px solid rgba(var(--line), .12);
}

.case-text p {
  margin-top: 14px;
  font-size: 16px;
}

.summary-panel {
  position: sticky;
  top: calc(var(--header-height) + 24px);
}

.summary-panel dl {
  margin-top: 18px;
}

.summary-panel dl > div {
  padding: 14px 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.contact-rows {
  display: grid;
  gap: 0;
  margin-top: 28px;
  padding: 8px 18px;
}

.contact-rows li {
  display: grid;
  grid-template-columns: 96px minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
  padding: 13px 0;
  border-top: 1px solid rgba(var(--line), .12);
}

.contact-rows span {
  color: var(--muted);
  font-size: 13px;
}

.copy-chip {
  min-height: 34px;
  padding: 7px 10px;
  border: 1px solid rgba(var(--line), .16);
  color: var(--text);
  background: var(--paper-strong);
  cursor: pointer;
}

.qr-frame {
  width: min(100%, 236px);
  margin: 20px auto;
  padding: 14px;
  border: 1px solid rgba(var(--line), .14);
  background: var(--paper-strong);
}

.site-footer {
  border-top: 1px solid rgba(var(--line), .12);
}

.footer-inner {
  min-height: 104px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  color: var(--muted);
  font-size: 13px;
}

.back-to-top {
  position: fixed;
  right: 22px;
  bottom: 22px;
  z-index: 40;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(var(--line), .18);
  border-radius: 4px;
  color: var(--accent-ink);
  background: var(--accent);
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s ease, transform .2s var(--ease);
}

.back-to-top.show {
  opacity: 1;
  pointer-events: auto;
}

.toast {
  position: fixed;
  left: 50%;
  bottom: 22px;
  z-index: 80;
  min-width: 140px;
  transform: translate(-50%, 10px);
  padding: 10px 14px;
  border-radius: 4px;
  color: var(--accent-ink);
  background: var(--accent);
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s ease, transform .2s var(--ease);
}

.toast.show {
  opacity: 1;
  transform: translate(-50%, 0);
}

.reveal-pending {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity .6s ease var(--reveal-delay, 0ms), transform .6s var(--ease) var(--reveal-delay, 0ms);
}

.reveal-pending.is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 1060px) {
  .hero-grid,
  .page-hero-grid,
  .contact-grid,
  .case-hero-grid,
  .method-grid,
  .about-grid,
  .lower-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .case-grid {
    grid-template-columns: 1fr;
  }

  .case-card,
  .case-card:first-child {
    min-height: auto;
    grid-template-columns: minmax(260px, .42fr) minmax(0, 1fr);
    grid-template-rows: auto;
  }

  .case-media {
    min-height: 100%;
  }

  .summary-panel {
    position: relative;
    top: auto;
  }
}

@media (max-width: 860px) {
  :root {
    --header-height: 66px;
  }

  .shell {
    width: min(100% - 32px, var(--site-width));
  }

  .header-inner,
  .site-header {
    min-height: var(--header-height);
  }

  .brand {
    grid-template-columns: 38px minmax(0, auto);
  }

  .brand-mark {
    width: 38px;
    height: 38px;
    font-size: 12px;
  }

  .brand-copy strong {
    font-size: 19px;
  }

  .brand-copy small {
    font-size: 11px;
  }

  .menu-toggle {
    display: grid;
  }

  .site-nav {
    position: fixed;
    left: 16px;
    right: 16px;
    top: calc(var(--header-height) + 10px);
    display: grid;
    gap: 2px;
    padding: 10px;
    border: 1px solid rgba(var(--line), .2);
    border-radius: 6px;
    background: var(--paper-strong);
    box-shadow: 0 28px 72px rgba(var(--shadow), .16);
    transform: translateY(-8px);
    opacity: 0;
    pointer-events: none;
  }

  .nav-open .site-nav {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .site-nav a {
    padding: 13px 12px;
  }

  .hero,
  .page-hero,
  .case-hero {
    min-height: auto;
    padding: 72px 0 64px;
  }

  .hero-bg {
    background:
      linear-gradient(180deg, var(--bg) 0%, rgba(255, 255, 255, .78) 52%, var(--bg) 100%),
      var(--page-image, url("assets/glass/hero.webp")) center top / cover no-repeat;
    opacity: .9;
  }

  h1 {
    font-size: clamp(54px, 16vw, 78px);
  }

  .page-copy h1,
  .case-intro h1 {
    font-size: clamp(40px, 12vw, 58px);
  }

  .hero-line,
  .page-subtitle {
    font-size: clamp(25px, 7vw, 34px);
  }

  .hero-summary,
  .page-copy > p:not(.breadcrumbs):not(.eyebrow):not(.page-subtitle),
  .case-intro > p:not(.breadcrumbs):not(.page-subtitle),
  .section-copy p {
    font-size: 16px;
  }

  .section {
    padding: 70px 0;
  }

  .section-head {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .text-link {
    justify-self: start;
  }

  .case-card,
  .case-card:first-child {
    grid-template-columns: 1fr;
    grid-template-rows: 214px auto;
  }

  .case-media {
    min-height: 214px;
  }

  .case-body {
    padding: 20px;
  }

  .case-metrics {
    grid-template-columns: 1fr;
  }

  .case-metrics div {
    padding-right: 0;
  }

  .metric-stack > div,
  .metric-stack > article {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .panel-portrait,
  .identity-chip {
    grid-template-columns: 62px minmax(0, 1fr);
    margin-top: 16px;
    padding: 6px 11px 6px 6px;
  }

  .panel-portrait img,
  .identity-chip img,
  .panel-portrait.compact img,
  .qr-panel .panel-portrait img {
    width: 62px;
    height: 62px;
  }

  .panel-portrait.compact,
  .qr-panel .panel-portrait {
    grid-template-columns: 62px minmax(0, 1fr);
  }

  .panel-portrait span,
  .identity-chip strong {
    font-size: 16px;
  }

  .teaser-panel {
    display: grid;
    padding: 24px;
  }

  .status-panel,
  .qr-panel,
  .method-aside,
  .result-panel,
  .summary-panel,
  .trust-panel,
  .talk-panel,
  .case-text {
    padding: 22px;
    width: 100%;
  }

  .timeline-panel {
    padding: 8px 22px;
  }

  .story-timeline > li {
    grid-template-columns: 24px minmax(0, 1fr);
    gap: 14px;
  }

  .story-timeline > li::before {
    left: 11px;
  }

  .case-takeaway article {
    grid-template-columns: 1fr;
    gap: 4px;
  }

  .contact-rows li {
    grid-template-columns: 1fr auto;
    gap: 8px 12px;
  }

  .contact-rows li > span {
    grid-column: 1 / -1;
  }

  .footer-inner {
    min-height: 88px;
    display: grid;
    align-content: center;
  }
}

@media (max-width: 430px) {
  .brand-copy small {
    display: none;
  }

  .hero-actions,
  .btn {
    width: 100%;
  }

  .contact-rows li {
    grid-template-columns: 1fr;
  }

  .copy-chip {
    width: fit-content;
  }
}
'''


def write_site(theme_key: str) -> None:
    theme = THEMES[theme_key]
    site_dir = EXPERIMENTS / theme["folder"]
    ensure_clean_dir(site_dir)
    copy_base_assets(site_dir)
    prepare_visuals(site_dir, theme_key)
    (site_dir / "cases").mkdir(parents=True, exist_ok=True)
    (site_dir / "style.css").write_text(css_for(), encoding="utf-8", newline="\n")
    (site_dir / "site.js").write_text(SITE_JS, encoding="utf-8", newline="\n")

    (site_dir / "index.html").write_text(
        page(
            "钟滔 | 新媒体运营案例集",
            "钟滔的新媒体运营案例集，聚焦内容、获客和转化，整理代表案例、个人经历与联系方式。",
            "https://www.xn--8bx391f.com/",
            "website",
            "home-page",
            "",
            "home",
            home_main(),
            theme["body"],
            PERSON_LD,
            is_home=True,
        ),
        encoding="utf-8",
        newline="\n",
    )
    about_ld = dict(PERSON_LD)
    about_ld["url"] = "https://www.xn--8bx391f.com/about.html"
    about_ld["description"] = "关于钟滔的完整介绍，整理个人经历、做事方式，以及现在在新媒体这个领域主要关注的事。"
    (site_dir / "about.html").write_text(
        page(
            "关于钟滔 | 经历、做事方式与现在在做的事",
            "关于钟滔的完整介绍，整理个人经历、做事方式，以及现在在新媒体这个领域主要关注的事。",
            "https://www.xn--8bx391f.com/about.html",
            "website",
            "about-page",
            "",
            "about",
            about_main(),
            theme["body"],
            about_ld,
        ),
        encoding="utf-8",
        newline="\n",
    )
    (site_dir / "contact.html").write_text(
        page(
            "联系钟滔 | 聊内容、获客或转化",
            "联系钟滔，沟通新媒体内容运营、内容获客、账号定位和转化复盘。",
            "https://www.xn--8bx391f.com/contact.html",
            "website",
            "contact-page",
            "",
            "contact",
            contact_main(),
            theme["body"],
            None,
            toast=True,
        ),
        encoding="utf-8",
        newline="\n",
    )

    for key, data in CASE_DATA.items():
        article_ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": data["title"].split(" | ")[0],
            "description": data["description"],
            "author": {"@type": "Person", "name": "钟滔", "url": "https://www.xn--8bx391f.com/about.html"},
            "mainEntityOfPage": data["canonical"],
        }
        (site_dir / "cases" / f"{key}.html").write_text(
            page(
                data["title"],
                data["description"],
                data["canonical"],
                "article",
                data["body"],
                "../",
                "cases",
                case_main(key),
                theme["body"],
                article_ld,
            ),
            encoding="utf-8",
            newline="\n",
        )


def write_preview() -> None:
    preview = r'''<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>钟滔网站实验版本预览</title>
    <meta name="description" content="钟滔个人网站的实验版式总入口，用于预览液态磨玻璃和极简方向的不同完整站点。" />
    <meta name="robots" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <meta name="googlebot" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <link rel="canonical" href="https://www.xn--8bx391f.com/experiments/" />
    <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        color: #201914;
        font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
        background:
          linear-gradient(90deg, rgba(30, 24, 19, .05) 0 1px, transparent 1px) 0 0 / 72px 72px,
          linear-gradient(0deg, rgba(30, 24, 19, .035) 0 1px, transparent 1px) 0 0 / 72px 72px,
          #f4eee4;
      }
      .shell {
        width: min(100% - 72px, 1220px);
        margin: 0 auto;
        padding: 58px 0;
      }
      header {
        display: grid;
        grid-template-columns: 132px minmax(0, 1fr);
        align-items: end;
        gap: 24px;
        max-width: 920px;
        margin-bottom: 42px;
      }
      .preview-identity {
        margin: 0;
        padding: 7px;
        border: 1px solid rgba(32, 25, 20, .16);
        border-radius: 6px;
        background: rgba(255, 252, 245, .72);
        box-shadow: 0 18px 40px rgba(69, 50, 32, .1);
      }
      .preview-identity img {
        display: block;
        width: 100%;
        aspect-ratio: 1;
        object-fit: cover;
        object-position: center 40%;
        border-radius: 4px;
      }
      .intro-copy {
        display: grid;
        gap: 14px;
      }
      .badge {
        width: fit-content;
        padding: 6px 10px;
        border: 1px solid rgba(32, 25, 20, .18);
        border-radius: 4px;
        color: #6d5b4c;
        background: rgba(255, 252, 245, .68);
        font-size: 13px;
      }
      h1, h2, h3, p { margin: 0; }
      h1 {
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: clamp(42px, 7vw, 96px);
        font-weight: 500;
        line-height: 1.08;
      }
      .lead {
        color: #74665a;
        font-size: 17px;
        line-height: 1.75;
      }
      .group + .group { margin-top: 42px; }
      .group-head {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 18px;
        padding-bottom: 16px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(32, 25, 20, .14);
      }
      .group h2 {
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: 30px;
        font-weight: 500;
      }
      .group-head p {
        color: #74665a;
        font-size: 14px;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
      }
      .grid.minimal {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
      .grid.portfolio {
        grid-template-columns: minmax(0, 1fr);
      }
      .card {
        position: relative;
        min-height: 450px;
        display: grid;
        grid-template-rows: 205px 1fr;
        overflow: hidden;
        border: 1px solid rgba(32, 25, 20, .13);
        border-radius: 6px;
        background: rgba(255, 252, 245, .82);
        box-shadow: 0 24px 60px rgba(69, 50, 32, .1);
      }
      .media {
        background: var(--image) center / cover no-repeat;
        border-bottom: 1px solid rgba(32, 25, 20, .1);
      }
      .body {
        display: grid;
        align-content: space-between;
        gap: 20px;
        padding: 22px;
      }
      .body h3 {
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: 28px;
        font-weight: 500;
      }
      .body p {
        margin-top: 10px;
        color: #76675a;
        font-size: 14px;
        line-height: 1.7;
      }
      a {
        color: inherit;
        text-decoration: none;
      }
      .button {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        min-height: 42px;
        padding: 9px 13px;
        border: 1px solid #211914;
        border-radius: 4px;
        color: #fffaf1;
        background: #211914;
        font-size: 14px;
      }
      .card.final::after {
        content: "当前推荐";
        position: absolute;
        top: 12px;
        right: 12px;
        padding: 5px 8px;
        border-radius: 4px;
        color: #211914;
        background: #f0c879;
        font-size: 12px;
      }
      .portfolio-card {
        min-height: 220px;
        grid-template-columns: 1fr;
        grid-template-rows: auto;
      }
      .portfolio-card .media {
        display: none;
      }
      .portfolio-card .body {
        align-content: center;
        min-height: 220px;
      }
      .portfolio-card .button {
        width: fit-content;
      }
      .button.is-disabled {
        color: #6d5b4c;
        background: rgba(255, 252, 245, .68);
        border-color: rgba(32, 25, 20, .18);
      }
      @media (max-width: 1040px) {
        .grid,
        .grid.minimal {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
      @media (max-width: 640px) {
        .shell {
          width: min(100% - 32px, 1220px);
          padding: 38px 0;
        }
        header {
          grid-template-columns: 82px minmax(0, 1fr);
          align-items: start;
          gap: 16px;
        }
        .group-head {
          display: grid;
        }
        .grid,
        .grid.minimal {
          grid-template-columns: 1fr;
        }
        .card {
          min-height: auto;
        }
        .portfolio-card {
          grid-template-columns: 1fr;
        }
        .portfolio-card .media {
          display: none;
        }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <header>
        <figure class="preview-identity">
          <img src="../assets/brand/portrait-zt-square.webp" alt="钟滔头像" loading="eager" decoding="async" />
        </figure>
        <div class="intro-copy">
          <span class="badge">线上预览 / 实验版本</span>
          <h1>钟滔网站视觉版本</h1>
          <p class="lead">上面保留液态磨玻璃方向，下面新增三套从简历 PDF 推导出来的极简方向。它们都是完整 5 页站点，可以直接进入每一版看首页、关于、案例和联系页。</p>
        </div>
      </header>

      <section class="group" aria-label="案例集入口">
        <div class="group-head">
          <h2>案例集入口</h2>
          <p>后续集中建设案例、项目和素材的位置，当前先保留入口。</p>
        </div>
        <div class="grid portfolio">
          <article class="card portfolio-card">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>案例集</h3><p>这里先收纳已经梳理出来的账号案例，后续再继续补项目过程、素材和复盘。</p></div><a class="button" href="portfolio.html">进入案例集</a></div>
          </article>
        </div>
      </section>

      <section class="group" aria-label="液态磨玻璃版本">
        <div class="group-head">
          <h2>液态磨玻璃</h2>
          <p>之前已完成的三版探索和最终候选，全部原样保留。</p>
        </div>
        <div class="grid">
          <article class="card final" style="--image: url('liquid-glass-final/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>Final</h3><p>黑金中文杂志感候选，细纹、纸感和液态玻璃层次已收紧。</p></div><a class="button" href="liquid-glass-final/index.html">打开 Final</a></div>
          </article>
          <article class="card" style="--image: url('liquid-glass-v1/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>V1</h3><p>清透、暖白、可信，更轻、更干净的个人品牌方向。</p></div><a class="button" href="liquid-glass-v1/index.html">打开 V1</a></div>
          </article>
          <article class="card" style="--image: url('liquid-glass-v2/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>V2</h3><p>黑金、纸感、中文杂志气质，是 final 的主要基础版本。</p></div><a class="button" href="liquid-glass-v2/index.html">打开 V2</a></div>
          </article>
          <article class="card" style="--image: url('liquid-glass-v3/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>V3</h3><p>更沉浸、更产品发布感，视觉冲击更强，内容路径仍保持清楚。</p></div><a class="button" href="liquid-glass-v3/index.html">打开 V3</a></div>
          </article>
        </div>
      </section>

      <section class="group" aria-label="极简简历风版本">
        <div class="group-head">
          <h2>极简简历风</h2>
          <p>从你的 10 套简历 PDF 里抽取配色、留白、细线和信息排版逻辑。</p>
        </div>
        <div class="grid minimal">
          <article class="card" style="--image: url('minimal-mono-focus/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>Mono Focus</h3><p>黑白聚焦、纸面留白、细线分区，像一份高级作品履历。</p></div><a class="button" href="minimal-mono-focus/index.html">打开 Mono</a></div>
          </article>
          <article class="card" style="--image: url('minimal-modern-blue/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>Modern Blue</h3><p>现代蓝清爽信息架构，偏 ATS clean 和 premium navy 的可信感。</p></div><a class="button" href="minimal-modern-blue/index.html">打开 Blue</a></div>
          </article>
          <article class="card" style="--image: url('minimal-warm-editorial/assets/glass/hero.webp')">
            <div class="media" aria-hidden="true"></div>
            <div class="body"><div><h3>Warm Editorial</h3><p>暖色杂志网格，保留简历的克制，但更有人味和纸感。</p></div><a class="button" href="minimal-warm-editorial/index.html">打开 Warm</a></div>
          </article>
        </div>
      </section>
    </main>
  </body>
</html>
'''
    (EXPERIMENTS / "preview.html").write_text(preview, encoding="utf-8", newline="\n")
    (EXPERIMENTS / "index.html").write_text(preview, encoding="utf-8", newline="\n")


def write_portfolio() -> None:
    portfolio = r'''<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>案例集账号归档 | 钟滔</title>
    <meta name="description" content="钟滔案例集账号归档，整理太希智能、杭州言心和杭州梦璃科技相关账号入口。" />
    <meta name="robots" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <meta name="googlebot" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <link rel="canonical" href="https://www.xn--8bx391f.com/experiments/portfolio.html" />
    <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        color: #201914;
        font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
        background:
          linear-gradient(90deg, rgba(30, 24, 19, .05) 0 1px, transparent 1px) 0 0 / 72px 72px,
          linear-gradient(0deg, rgba(30, 24, 19, .035) 0 1px, transparent 1px) 0 0 / 72px 72px,
          #f4eee4;
      }
      a { color: inherit; text-decoration: none; }
      .shell {
        width: min(100% - 72px, 1180px);
        margin: 0 auto;
        padding: 54px 0 68px;
      }
      .top-links {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
      .top-link {
        display: inline-flex;
        align-items: center;
        min-height: 38px;
        padding: 7px 10px;
        border: 1px solid rgba(32, 25, 20, .16);
        border-radius: 4px;
        color: #6d5b4c;
        background: rgba(255, 252, 245, .68);
        font-size: 13px;
      }
      header {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(248px, 320px);
        align-items: end;
        gap: 28px;
        margin-top: 34px;
        padding-bottom: 32px;
        border-bottom: 1px solid rgba(32, 25, 20, .14);
      }
      h1, h2, h3, p { margin: 0; }
      h1 {
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: clamp(46px, 8vw, 104px);
        font-weight: 500;
        line-height: 1.05;
      }
      .lead {
        max-width: 720px;
        margin-top: 18px;
        color: #74665a;
        font-size: 17px;
        line-height: 1.78;
      }
      .portrait {
        margin: 0;
        display: grid;
        grid-template-columns: 66px minmax(0, 1fr);
        align-items: center;
        gap: 14px;
        padding: 12px 14px;
        border: 1px solid rgba(32, 25, 20, .16);
        border-radius: 6px;
        background:
          linear-gradient(135deg, rgba(255, 252, 245, .9), rgba(244, 238, 228, .72)),
          linear-gradient(90deg, rgba(32, 25, 20, .05) 0 1px, transparent 1px) 0 0 / 24px 24px;
        box-shadow: 0 18px 40px rgba(69, 50, 32, .08);
      }
      .portrait img {
        display: block;
        width: 66px;
        height: 66px;
        aspect-ratio: 1;
        object-fit: cover;
        object-position: center 36%;
        border: 1px solid rgba(32, 25, 20, .18);
        border-radius: 999px;
        filter: saturate(.9) contrast(.98);
      }
      .portrait figcaption {
        display: grid;
        gap: 3px;
        min-width: 0;
      }
      .portrait strong {
        color: #201914;
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: 20px;
        font-weight: 500;
        line-height: 1.15;
      }
      .portrait span {
        color: #6f5f52;
        font-size: 12px;
        line-height: 1.55;
      }
      .summary {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 28px 0 34px;
      }
      .summary article,
      .project {
        border: 1px solid rgba(32, 25, 20, .13);
        border-radius: 6px;
        background: rgba(255, 252, 245, .82);
        box-shadow: 0 22px 54px rgba(69, 50, 32, .08);
      }
      .summary article {
        padding: 18px 20px;
      }
      .summary strong {
        display: block;
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: 30px;
        font-weight: 500;
        line-height: 1;
      }
      .summary span {
        display: block;
        margin-top: 8px;
        color: #74665a;
        font-size: 13px;
      }
      .projects {
        display: grid;
        gap: 18px;
      }
      .project {
        display: grid;
        grid-template-columns: minmax(220px, .34fr) minmax(0, 1fr);
        overflow: hidden;
      }
      .project-head {
        min-height: 100%;
        padding: 28px;
        border-right: 1px solid rgba(32, 25, 20, .1);
        background:
          linear-gradient(135deg, rgba(32, 25, 20, .82), rgba(32, 25, 20, .28)),
          linear-gradient(90deg, rgba(255, 252, 245, .16) 0 1px, transparent 1px) 0 0 / 26px 26px,
          linear-gradient(0deg, rgba(255, 252, 245, .1) 0 1px, transparent 1px) 0 0 / 26px 26px;
        color: #fffaf1;
      }
      .project-head span {
        color: rgba(255, 250, 241, .68);
        font-size: 13px;
      }
      .project-head h2 {
        margin-top: 14px;
        font-family: "Noto Serif SC", "Songti SC", serif;
        font-size: 34px;
        font-weight: 500;
        line-height: 1.16;
      }
      .project-head p {
        margin-top: 16px;
        color: rgba(255, 250, 241, .72);
        font-size: 14px;
        line-height: 1.72;
      }
      .accounts {
        display: grid;
        gap: 0;
        padding: 0 28px;
      }
      .account {
        display: grid;
        grid-template-columns: 112px minmax(0, 1fr) auto;
        align-items: center;
        gap: 18px;
        min-height: 94px;
        padding: 18px 0;
        border-top: 1px solid rgba(32, 25, 20, .1);
      }
      .account:first-child { border-top: 0; }
      .platform {
        width: fit-content;
        padding: 5px 9px;
        border: 1px solid rgba(32, 25, 20, .16);
        border-radius: 4px;
        color: #6d5b4c;
        background: rgba(244, 238, 228, .72);
        font-size: 13px;
      }
      .account strong {
        display: block;
        color: #201914;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.35;
      }
      .account small {
        display: block;
        margin-top: 4px;
        color: #76675a;
        font-size: 13px;
        line-height: 1.5;
      }
      .open {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        min-height: 40px;
        padding: 8px 12px;
        border: 1px solid #211914;
        border-radius: 4px;
        color: #fffaf1;
        background: #211914;
        font-size: 13px;
        white-space: nowrap;
      }
      .search-note {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        min-height: 40px;
        padding: 8px 12px;
        border: 1px solid rgba(32, 25, 20, .18);
        border-radius: 4px;
        color: #6d5b4c;
        background: rgba(244, 238, 228, .76);
        font-size: 13px;
        white-space: nowrap;
      }
      @media (max-width: 840px) {
        .shell { width: min(100% - 32px, 1180px); padding-top: 38px; }
        header { grid-template-columns: 1fr; }
        .portrait {
          width: min(100%, 320px);
          grid-template-columns: 58px minmax(0, 1fr);
          align-self: start;
        }
        .portrait img {
          width: 58px;
          height: 58px;
        }
        .summary { grid-template-columns: 1fr; }
        .project { grid-template-columns: 1fr; }
        .project-head { border-right: 0; border-bottom: 1px solid rgba(32, 25, 20, .1); }
        .accounts { padding: 0 20px; }
        .account { grid-template-columns: 1fr; gap: 10px; align-items: start; }
        .open,
        .search-note { width: fit-content; }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <nav class="top-links" aria-label="案例集快捷入口">
        <a class="top-link" href="minimal-modern-blue/index.html">返回个人站</a>
        <a class="top-link" href="https://my.feishu.cn/wiki/NLwjw7TsIiR8ZZkBZDzcEUHdneh" target="_blank" rel="noopener noreferrer">飞书案例集</a>
      </nav>
      <header>
        <div>
          <h1>案例集账号归档</h1>
        </div>
        <figure class="portrait">
          <img src="../assets/brand/portrait-zt-square.webp" alt="钟滔头像" loading="eager" decoding="async" />
          <figcaption>
            <strong>钟滔</strong>
            <span>新媒体运营案例集<br />账号入口归档</span>
          </figcaption>
        </figure>
      </header>

      <section class="summary" aria-label="账号归档概览">
        <article><strong>3</strong><span>项目 / 品牌</span></article>
        <article><strong>11</strong><span>账号入口</span></article>
        <article><strong>3</strong><span>主要平台</span></article>
      </section>

      <section class="projects" aria-label="账号列表">
        <article class="project">
          <div class="project-head">
            <span>01 / 科技产品传播</span>
            <h2>太希智能</h2>
            <p>围绕外骨骼机器人与科技产品传播沉淀的账号入口。</p>
          </div>
          <div class="accounts">
            <div class="account">
              <span class="platform">抖音</span>
              <div><strong>太希智行外骨骼官方号</strong><small>科技产品传播 / 外骨骼机器人</small></div>
              <a class="open" href="https://www.douyin.com/user/MS4wLjABAAAAbudLV8XIBBPDe75KXmXyMX6e8sbgEk7iuypt90v-2MA?from_tab_name=main" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>杭州太希智能科技</strong><small>科技产品传播 / 内容矩阵</small></div>
              <a class="open" href="https://www.xiaohongshu.com/user/profile/65b0c35c000000000d03fa49?xsec_token=ABkU6LkemMfs4mOXAqShXC-Ubr9b0d-tpgHBJuvpBOopI%3D&amp;xsec_source=pc_search" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">微信</span>
              <div><strong>公众号 / 视频号</strong><small>微信搜索：太希智能</small></div>
              <span class="search-note">微信搜索</span>
            </div>
            <div class="account">
              <span class="platform">抖音</span>
              <div><strong>广交会外骨骼搜索结果</strong><small>抖音搜索结果 / 传播延展</small></div>
              <a class="open" href="https://www.douyin.com/jingxuan/search/%E5%B9%BF%E4%BA%A4%E4%BC%9A%E5%A4%96%E9%AA%A8%E9%AA%BC?aid=c965de21-5225-40a0-b57e-989575e98d36&amp;type=general" target="_blank" rel="noopener noreferrer">查看结果</a>
            </div>
          </div>
        </article>

        <article class="project">
          <div class="project-head">
            <span>02 / 同城教育获客</span>
            <h2>杭州言心</h2>
            <p>围绕口才培训、本地教育和同城线索承接沉淀的账号入口。</p>
          </div>
          <div class="accounts">
            <div class="account">
              <span class="platform">抖音</span>
              <div><strong>言心口才培训</strong><small>口才培训 / 同城获客</small></div>
              <a class="open" href="https://www.douyin.com/user/MS4wLjABAAAAjr1EmrrfY44sXZkiAAqYjRcID4QGRPZAGPuHh6GwLE3tqTWj84CF8r00VW1ru27e?from_tab_name=main" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>跟言心-韩老师学口才</strong><small>表达训练 / 小红书搜索</small></div>
              <a class="open" href="https://www.xiaohongshu.com/user/profile/6725f78b000000001d02e3eb?xsec_token=ABR2EIWyGZUSOlQdHloOq60ohO76NT8TdFVMNPl0yidhE%3D&amp;xsec_source=pc_search" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>Back To Me｜见自己</strong><small>表达成长 / 内容承接</small></div>
              <a class="open" href="https://www.xiaohongshu.com/user/profile/69a23cea000000001d00402a?xsec_token=ABDvX_pqytS4NuRNIY8_8jYKywZfZMDIc_Tk_Rh7wyp-8=&amp;xsec_source=pc_comment" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>杭州口才老师-阿楠</strong><small>杭州口才 / 本地线索</small></div>
              <a class="open" href="https://www.xiaohongshu.com/user/profile/689beb42000000001900c55a?xsec_token=AB_2gILMGjiVHUWflGTcrFefhQar3nZTxeFMuuHyqlsNo%3D&amp;xsec_source=pc_search" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>学口才的阿成</strong><small>口才表达 / 小红书搜索</small></div>
              <a class="open" href="https://xhslink.com/m/A9M3vAXEtZL" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>舒言｜杭州成人口才</strong><small>成人口才 / 杭州本地</small></div>
              <a class="open" href="https://xhslink.com/m/3MzZSFn7NiE" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
          </div>
        </article>

        <article class="project">
          <div class="project-head">
            <span>03 / 美业 IP 内容</span>
            <h2>杭州梦璃科技</h2>
            <p>围绕美业 IP、内容表达和账号运营沉淀的账号入口。</p>
          </div>
          <div class="accounts">
            <div class="account">
              <span class="platform">小红书</span>
              <div><strong>王梦璃在美业</strong><small>美业 IP / 内容运营</small></div>
              <a class="open" href="https://www.xiaohongshu.com/user/profile/65e82628000000000500a346?xsec_token=ABeHYrAMs09yggeQ0EhsaYyEu-fV5i4iFQ5v2NknvYP8M%3D&amp;xsec_source=pc_search" target="_blank" rel="noopener noreferrer">打开账号</a>
            </div>
          </div>
        </article>
      </section>
    </main>
  </body>
</html>
'''
    (EXPERIMENTS / "portfolio.html").write_text(portfolio, encoding="utf-8", newline="\n")


def main() -> None:
    for variant in THEMES:
        write_site(variant)
    write_preview()
    write_portfolio()
    print("Generated minimal resume-inspired experiments:")
    for variant, theme in THEMES.items():
        print(f"- {variant}: {EXPERIMENTS / theme['folder']}")


if __name__ == "__main__":
    main()
