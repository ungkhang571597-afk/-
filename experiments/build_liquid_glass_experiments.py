from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
GENERATED = Path(
    r"C:\Users\ZHONGTAO\.codex\generated_images\019eff09-c49c-7610-b21f-8b467bae58eb"
)

SOURCE_IMAGES = {
    "v1": {
        "hero": GENERATED / "ig_05c10aafe43f8a54016a3d76e3d61481988f953abf13a658eb.png",
        "taixi": GENERATED / "ig_05c10aafe43f8a54016a3d7712bb348198a05fcb818fec964a.png",
        "yanxin": GENERATED / "ig_05c10aafe43f8a54016a3d773db5c08198b2654a6e2d8adb78.png",
        "mengli": GENERATED / "ig_05c10aafe43f8a54016a3d7777001c81989e66413c78af8c2c.png",
        "contact": GENERATED / "ig_05c10aafe43f8a54016a3d77a0e3c481988027818038258dd4.png",
    },
    "v2": {
        "hero": GENERATED / "ig_05c10aafe43f8a54016a3d77d4bd908198a6e2f2bdf2ac034a.png",
        "taixi": ROOT / "assets" / "brand" / "case-taixi-card-v2.webp",
        "yanxin": ROOT / "assets" / "brand" / "case-yanxin-card-v2.webp",
        "mengli": ROOT / "assets" / "brand" / "case-mengli-card-v2.webp",
        "contact": GENERATED / "ig_05c10aafe43f8a54016a3d7813395c81989286b206b25a47b4.png",
    },
    "v3": {
        "hero": GENERATED / "ig_05c10aafe43f8a54016a3d78520884819893c64be33d755170.png",
        "taixi": GENERATED / "ig_05c10aafe43f8a54016a3d789789c48198b9aa4b6c6eb9fd27.png",
        "yanxin": GENERATED / "ig_05c10aafe43f8a54016a3d78d5d8148198acc51fdda264fa89.png",
        "mengli": GENERATED / "ig_05c10aafe43f8a54016a3d79193d68819882e69a0018800229.png",
        "contact": GENERATED / "ig_05c10aafe43f8a54016a3d795a78d88198b713130baaf2ef92.png",
    },
    "final": {
        "hero": GENERATED / "ig_05c10aafe43f8a54016a3d77d4bd908198a6e2f2bdf2ac034a.png",
        "taixi": ROOT / "assets" / "brand" / "case-taixi-card-v2.webp",
        "yanxin": ROOT / "assets" / "brand" / "case-yanxin-card-v2.webp",
        "mengli": ROOT / "assets" / "brand" / "case-mengli-card-v2.webp",
        "contact": GENERATED / "ig_05c10aafe43f8a54016a3d7813395c81989286b206b25a47b4.png",
    },
}

THEMES = {
    "v1": {
        "folder": "liquid-glass-v1",
        "name": "Apple Clean Trust",
        "body": "theme-clean",
        "vars": {
            "bg": "#f6f1e8",
            "bg2": "#ebe2d5",
            "text": "#15120e",
            "muted": "#6b6258",
            "soft": "#8f8171",
            "accent": "#b88238",
            "accent2": "#d6b16c",
            "surface": "255, 252, 245",
            "surfaceStrong": "255, 250, 239",
            "surfaceAlpha": "0.68",
            "surfaceStrongAlpha": "0.86",
            "line": "70, 54, 31",
            "lineAlpha": "0.16",
            "shadow": "77, 55, 26",
            "shadowAlpha": "0.18",
            "nav": "rgba(255, 252, 245, 0.72)",
            "imageOpacity": "0.58",
            "scrim": "linear-gradient(90deg, rgba(246,241,232,0.96) 0%, rgba(246,241,232,0.82) 43%, rgba(246,241,232,0.34) 72%, rgba(246,241,232,0.78) 100%)",
        },
    },
    "v2": {
        "folder": "liquid-glass-v2",
        "name": "Black Gold Editorial",
        "body": "theme-editorial",
        "vars": {
            "bg": "#0d0a07",
            "bg2": "#1a130d",
            "text": "#fff5df",
            "muted": "#d2c2a2",
            "soft": "#a79370",
            "accent": "#d2a04e",
            "accent2": "#f0c779",
            "surface": "27, 23, 17",
            "surfaceStrong": "38, 31, 22",
            "surfaceAlpha": "0.62",
            "surfaceStrongAlpha": "0.86",
            "line": "255, 230, 181",
            "lineAlpha": "0.17",
            "shadow": "0, 0, 0",
            "shadowAlpha": "0.42",
            "nav": "rgba(16, 12, 8, 0.72)",
            "imageOpacity": "0.46",
            "scrim": "linear-gradient(90deg, rgba(13,10,7,0.98) 0%, rgba(13,10,7,0.86) 42%, rgba(13,10,7,0.42) 74%, rgba(13,10,7,0.9) 100%)",
        },
    },
    "v3": {
        "folder": "liquid-glass-v3",
        "name": "Immersive Product Glass",
        "body": "theme-immersive",
        "vars": {
            "bg": "#070707",
            "bg2": "#101213",
            "text": "#fbf1e3",
            "muted": "#c9baa5",
            "soft": "#958778",
            "accent": "#c89a61",
            "accent2": "#f1c684",
            "surface": "15, 16, 16",
            "surfaceStrong": "25, 27, 27",
            "surfaceAlpha": "0.58",
            "surfaceStrongAlpha": "0.84",
            "line": "255, 231, 194",
            "lineAlpha": "0.15",
            "shadow": "0, 0, 0",
            "shadowAlpha": "0.5",
            "nav": "rgba(8, 9, 9, 0.72)",
            "imageOpacity": "0.54",
            "scrim": "linear-gradient(90deg, rgba(7,7,7,0.98) 0%, rgba(7,7,7,0.8) 39%, rgba(7,7,7,0.28) 72%, rgba(7,7,7,0.9) 100%)",
        },
    },
    "final": {
        "folder": "liquid-glass-final",
        "name": "Final Black Gold Magazine Glass",
        "body": "theme-final",
        "vars": {
            "bg": "#0b0907",
            "bg2": "#17110c",
            "text": "#fff6e6",
            "muted": "#d8c7a7",
            "soft": "#aa9675",
            "accent": "#d09a45",
            "accent2": "#f1c978",
            "surface": "25, 21, 16",
            "surfaceStrong": "37, 30, 22",
            "surfaceAlpha": "0.66",
            "surfaceStrongAlpha": "0.9",
            "line": "255, 229, 177",
            "lineAlpha": "0.18",
            "shadow": "0, 0, 0",
            "shadowAlpha": "0.48",
            "nav": "rgba(13, 10, 7, 0.82)",
            "imageOpacity": "0.5",
            "scrim": "linear-gradient(90deg, rgba(11,9,7,0.98) 0%, rgba(11,9,7,0.85) 39%, rgba(11,9,7,0.4) 72%, rgba(11,9,7,0.9) 100%)",
        },
    },
}

CONTACT = {
    "email": "ZT3956@126.com",
    "phone": "18707073956",
    "region": "杭州 / 赣州",
}


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def save_webp(src: Path, dest: Path, max_size: tuple[int, int] = (1800, 1125)) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as image:
        image = image.convert("RGB")
        image.thumbnail(max_size, Image.LANCZOS)
        image.save(dest, "WEBP", quality=84, method=6)


def copy_static_assets(site_dir: Path, variant: str) -> None:
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
    for key, src in SOURCE_IMAGES[variant].items():
        save_webp(src, site_dir / "assets" / "glass" / f"{key}.webp")


def json_script(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=8)


def head(
    title: str,
    description: str,
    canonical: str,
    og_type: str,
    prefix: str,
    jsonld: dict | None,
    is_home: bool = False,
) -> str:
    preload = ""
    baidu = ""
    if is_home:
        preload = '    <link rel="preload" href="assets/glass/hero.webp" as="image" type="image/webp" fetchpriority="high" />\n'
        baidu = '    <meta name="baidu-site-verification" content="codeva-aoCpendozd" />\n'
    ld = ""
    if jsonld:
        ld = f'    <script type="application/ld+json">\n{json_script(jsonld)}\n    </script>\n'
    return f"""  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="robots" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <meta name="googlebot" content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <meta name="theme-color" content="#0b0d0c" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:site_name" content="钟滔" />
    <meta property="og:locale" content="zh_CN" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="https://www.xn--8bx391f.com/assets/brand/og-cover.jpg" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="https://www.xn--8bx391f.com/assets/brand/og-cover.jpg" />
{baidu}    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml" />
{preload}    <link rel="stylesheet" href="{prefix}style.css" />
{ld}  </head>"""


def nav(prefix: str, current: str, home_page: bool = False) -> str:
    home_href = "#home" if home_page else f"{prefix}index.html"
    cases_href = "#cases" if home_page else f"{prefix}index.html#cases"
    brand_href = "#home" if home_page else f"{prefix}index.html"

    def current_attr(key: str) -> str:
        return ' class="is-current" aria-current="page"' if current == key else ""

    return f"""    <header class="site-header" aria-label="站点头部">
      <div class="shell header-inner">
        <a class="brand" href="{brand_href}" aria-label="返回首页">
          <span class="brand-mark">ZT</span>
          <span class="brand-copy">
            <strong>钟滔</strong>
            <small>新媒体运营 / 案例集</small>
          </span>
        </a>

        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
          <span></span>
          <span></span>
          <span></span>
          <span class="sr-only">打开导航</span>
        </button>

        <nav class="site-nav" id="site-nav" aria-label="主导航">
          <a href="{home_href}"{current_attr("home")}>首页</a>
          <a href="{cases_href}"{current_attr("cases")}>案例</a>
          <a href="https://my.feishu.cn/wiki/NLwjw7TsIiR8ZZkBZDzcEUHdneh" target="_blank" rel="noopener noreferrer">飞书案例集</a>
          <a href="{prefix}about.html"{current_attr("about")}>关于</a>
          <a href="{prefix}contact.html"{current_attr("contact")}>联系</a>
        </nav>
      </div>
    </header>"""


def footer(prefix: str, toast: bool = False) -> str:
    toast_html = '\n    <div id="toast" class="toast" aria-live="polite" aria-atomic="true" role="status"></div>' if toast else ""
    return f"""    <footer class="site-footer" aria-label="页脚">
      <div class="shell footer-inner">
        <p>&copy; <span id="year">2025</span> 钟滔</p>
        <p class="footer-note">新媒体运营 / 案例集</p>
      </div>
    </footer>
{toast_html}
    <button id="back-to-top" class="back-to-top" type="button" aria-label="回到顶部">↑</button>
    <script src="{prefix}site.js"></script>"""


def page(
    title: str,
    description: str,
    canonical: str,
    og_type: str,
    body_class: str,
    prefix: str,
    current: str,
    main: str,
    theme_body: str,
    jsonld: dict | None = None,
    is_home: bool = False,
    toast: bool = False,
) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
{head(title, description, canonical, og_type, prefix, jsonld, is_home)}
  <body class="{theme_body} {body_class}">
{nav(prefix, current, is_home)}
{main}
{footer(prefix, toast)}
  </body>
</html>
"""


PERSON_LD = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "钟滔",
    "alternateName": "Zhong Tao",
    "url": "https://www.xn--8bx391f.com/",
    "image": "https://www.xn--8bx391f.com/assets/brand/portrait-zt-square.webp",
    "description": "钟滔的新媒体运营案例集，聚焦内容、获客和转化。",
    "jobTitle": "新媒体运营",
    "email": "mailto:ZT3956@126.com",
    "telephone": "+86-18707073956",
    "knowsAbout": ["新媒体运营", "内容运营", "内容获客", "小红书 SEO", "抖音内容", "信息流", "科技产品传播", "AI 提效"],
    "homeLocation": {"@type": "Place", "name": "杭州"},
}


def home_main() -> str:
    return """    <main id="main-content">
      <section class="hero home-hero" id="home" aria-label="首页首屏">
        <div class="hero-bg" aria-hidden="true"></div>
        <div class="shell hero-grid">
          <div class="hero-copy reveal-on-scroll">
            <p class="eyebrow">新媒体运营 / 案例集</p>
            <h1>钟滔</h1>
            <p class="hero-line">内容、获客、转化</p>
            <p class="hero-summary">目前主要在新媒体领域，做内容传播、线索承接和转化复盘，也在尝试用 AI 工具把运营流程跑得更稳。</p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="#cases">看代表案例 <span aria-hidden="true">→</span></a>
              <a class="btn btn-ghost" href="contact.html">联系我 <span aria-hidden="true">→</span></a>
            </div>
          </div>

          <aside class="hero-panel glass-panel reveal-on-scroll" aria-label="关键结果">
            <p class="eyebrow">可被复盘的结果</p>
            <figure class="panel-portrait">
              <img src="assets/brand/portrait-zt-card.webp" alt="钟滔头像" loading="eager" decoding="async" />
              <figcaption><span>钟滔</span><small>新媒体运营 / 内容获客</small></figcaption>
            </figure>
            <div class="metric-stack">
              <div><strong>2900+</strong><span>同城商家累计获客</span></div>
              <div><strong>216 万</strong><span>12 个月 GMV</span></div>
              <div><strong>20%</strong><span>自然流转化率</span></div>
            </div>
          </aside>
        </div>
      </section>

      <section class="section cases-section" id="cases" aria-label="代表案例">
        <div class="shell">
          <div class="section-head">
            <p class="eyebrow">代表案例</p>
            <h2>不是把内容做热闹，而是把结果接起来</h2>
            <a class="text-link" href="about.html#taixi-smart">看太希经历 <span aria-hidden="true">→</span></a>
          </div>

          <div class="case-grid">
            <article class="case-card glass-card case-taixi reveal-on-scroll">
              <a class="card-hit" href="about.html#taixi-smart" aria-label="查看杭州太希智能经历"></a>
              <div class="case-media" aria-hidden="true"></div>
              <div class="case-body">
                <span class="case-tag">科技产品传播</span>
                <h3>杭州太希智能</h3>
                <p>从 0 到 1 搭建新媒体矩阵，围绕外骨骼机器人做内容传播、线索承接、跨部门协同和 AI 提效。</p>
                <div class="case-metrics">
                  <div><strong>20亿+</strong><span>全网曝光</span></div>
                  <div><strong>3000+</strong><span>C 端线索</span></div>
                  <div><strong>900+</strong><span>B 端意向</span></div>
                </div>
              </div>
            </article>

            <article class="case-card glass-card case-yanxin reveal-on-scroll">
              <a class="card-hit" href="cases/yanxin.html" aria-label="查看杭州言心口才案例"></a>
              <div class="case-media" aria-hidden="true"></div>
              <div class="case-body">
                <span class="case-tag">同城获客</span>
                <h3>杭州言心口才</h3>
                <p>本地口才/演讲培训项目，重点不是内容热闹，而是把小红书 SEO、抖音自然流和私域承接串起来。</p>
                <div class="case-metrics">
                  <div><strong>800+</strong><span>小红书线索</span></div>
                  <div><strong>2100+</strong><span>抖音获客</span></div>
                  <div><strong>20%</strong><span>自然流转化率</span></div>
                </div>
              </div>
            </article>

            <article class="case-card glass-card case-mengli reveal-on-scroll">
              <a class="card-hit" href="cases/mengli.html" aria-label="查看梦璃美业 IP 案例"></a>
              <div class="case-media" aria-hidden="true"></div>
              <div class="case-body">
                <span class="case-tag">美业 IP 运营</span>
                <h3>梦璃美业 IP</h3>
                <p>围绕选题拆解、内容表达、数据复盘和获客转化，让账号表达稳定地产生结果。</p>
                <div class="case-metrics">
                  <div><strong>1200+</strong><span>累计获客</span></div>
                  <div><strong>120 万</strong><span>6 个月 GMV</span></div>
                  <div><strong>30%</strong><span>完播率提升</span></div>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="section method-section" aria-label="做事方式">
        <div class="shell method-grid">
          <div class="section-copy">
            <p class="eyebrow">做事方式</p>
            <h2>先看结果，再做内容，持续复盘</h2>
            <p>我更习惯把内容放进完整链路里看：用户从哪里看到，为什么愿意留下线索，后面怎么承接，最后能不能变成可复盘的结果。</p>
          </div>
          <div class="method-list glass-panel">
            <article><span>01</span><strong>先看结果</strong><p>先想清楚要达成什么，再决定内容方向和动作。</p></article>
            <article><span>02</span><strong>再做内容</strong><p>内容不是越多越好，而是为线索和转化服务。</p></article>
            <article><span>03</span><strong>持续复盘</strong><p>用数据和实际反馈修正节奏，不靠感觉硬推。</p></article>
          </div>
        </div>
      </section>

      <section class="section contact-teaser" aria-label="联系入口">
        <div class="shell teaser-panel glass-card">
          <div>
            <p class="eyebrow">CONTACT</p>
            <h2>如果你想找我聊</h2>
            <p>聊内容、获客或转化，可以直接发起一次简短沟通。</p>
          </div>
          <a class="btn btn-primary" href="contact.html">进入联系页 <span aria-hidden="true">→</span></a>
        </div>
      </section>
    </main>
"""


def about_main() -> str:
    return """    <main id="main-content">
      <section class="page-hero about-hero" aria-label="关于钟滔">
        <div class="hero-bg" aria-hidden="true"></div>
        <div class="shell page-hero-grid">
          <div class="page-copy reveal-on-scroll">
            <p class="breadcrumbs"><a href="index.html">首页</a> / 关于</p>
            <h1>关于钟滔</h1>
            <p class="page-subtitle">做过销售，也当过兵，现在主要在新媒体领域继续往前走</p>
            <p>这一页把我一路走过来的几个节点、现在怎么看内容这件事，以及我更习惯怎么做事，完整放在一起。</p>
          </div>
          <aside class="status-panel glass-panel reveal-on-scroll">
            <p class="eyebrow">现在的状态</p>
            <figure class="panel-portrait">
              <img src="assets/brand/portrait-zt-square.webp" alt="钟滔头像" loading="eager" decoding="async" />
              <figcaption><span>钟滔</span><small>杭州 / 新媒体运营</small></figcaption>
            </figure>
            <strong>新媒体 / 科技产品传播</strong>
            <span>目前在太希智能做新媒体矩阵、内容增长和线索承接</span>
            <hr />
            <strong>杭州 / 赣州</strong>
            <span>平时微信看得更多，沟通比较直接</span>
          </aside>
        </div>
      </section>

      <section class="section about-story" aria-label="经历线">
        <div class="shell about-grid">
          <article class="timeline-panel glass-panel reveal-on-scroll">
            <ol class="story-timeline">
              <li><span></span><div><h2>学生时期</h2><p>学生时期摆过摊，第一次觉得自己可以靠自己往前走。</p></div></li>
              <li><span></span><div><h2>19 岁出省</h2><p>带着五百块第一次出省，一路走下来，越来越不相信“把话说满”这件事。</p></div></li>
              <li><span></span><div><h2>B 端销售</h2><p>第一次真正意识到：客户要的不是听起来厉害的方案，而是可执行、能见效的结果。</p></div></li>
              <li><span></span><div><h2>服役两年</h2><p>这段经历让我学会了纪律、协作和长期主义，也让我更能扛住压力和不确定性。</p></div></li>
              <li><span></span><div><h2>新媒体运营</h2><p>回到内容和流量这件事上，我更关注从内容、获客到转化的全链路能不能跑通、跑稳。</p></div></li>
              <li class="is-current" id="taixi-smart"><span></span><div><h2>太希智能</h2><p>在杭州太希智能负责新媒体矩阵从 0 到 1，围绕外骨骼机器人做内容传播、线索承接和跨部门协同，也开始把内容、项目和效率工具放到同一条链路里看。</p><ul class="proof-list"><li>抖音、小红书、视频号、公众号矩阵搭建</li><li>3000+ C 端线索，900+ B 端意向</li><li>AI 自动化报表把统计工作从约 2 小时压到 3 分钟</li></ul></div></li>
            </ol>
          </article>

          <aside class="method-aside glass-card reveal-on-scroll">
            <h2>做事方式</h2>
            <div class="compact-list">
              <article><strong>先看结果</strong><p>先想清楚要达成什么结果，再决定内容和动作。</p></article>
              <article><strong>再做内容</strong><p>内容不是越多越好，而是为结果服务。</p></article>
              <article><strong>持续复盘</strong><p>定期复盘数据和动作，不断优化节奏和方向。</p></article>
            </div>
          </aside>
        </div>
      </section>
    </main>
"""


def contact_main() -> str:
    return f"""    <main id="main-content">
      <section class="page-hero contact-hero" aria-label="联系钟滔">
        <div class="hero-bg" aria-hidden="true"></div>
        <div class="shell contact-grid">
          <div class="page-copy reveal-on-scroll">
            <p class="eyebrow">CONTACT</p>
            <h1>如果你想找我聊</h1>
            <p class="page-subtitle">聊内容、获客或转化</p>
            <p>我目前专注新媒体内容运营与增长，帮助项目从内容走到结果。如果你有相关需求或想法，欢迎发起一次简短沟通。</p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="#wechat">扫码加微信 <span aria-hidden="true">→</span></a>
              <a class="btn btn-ghost" href="index.html#cases">看代表案例 <span aria-hidden="true">→</span></a>
            </div>

            <ul class="contact-rows glass-panel">
              <li><span>邮箱</span><a id="email-text" href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a><button class="copy-chip" type="button" data-copy="#email-text">复制</button></li>
              <li><span>微信 / 手机</span><a id="phone-text" href="tel:{CONTACT["phone"]}">{CONTACT["phone"]}</a><button class="copy-chip" type="button" data-copy="#phone-text">复制</button></li>
              <li><span>地区</span><strong>{CONTACT["region"]}</strong></li>
            </ul>
          </div>

          <aside class="qr-panel glass-card reveal-on-scroll" id="wechat" aria-label="微信二维码">
            <p class="eyebrow">微信联系</p>
            <figure class="panel-portrait compact">
              <img src="assets/brand/portrait-zt-square.webp" alt="钟滔头像" loading="eager" decoding="async" />
              <figcaption><span>钟滔</span><small>通常当天回复</small></figcaption>
            </figure>
            <h2>扫码添加微信</h2>
            <div class="qr-frame">
              <img src="assets/brand/wechat-qr-mono.png" alt="钟滔的微信二维码" loading="eager" decoding="async" />
            </div>
            <p>添加时备注来意，通常当天回复。</p>
          </aside>
        </div>
      </section>

      <section class="section contact-lower" aria-label="适合聊什么">
        <div class="shell lower-grid">
          <div class="talk-panel glass-panel reveal-on-scroll">
            <h2>适合聊什么</h2>
            <div class="compact-list">
              <article><strong>账号定位</strong><p>理清账号定位与人设，找到差异化方向。</p></article>
              <article><strong>内容获客</strong><p>用内容吸引精准用户，带来持续线索。</p></article>
              <article><strong>转化复盘</strong><p>梳理转化链路，优化动作，提升结果。</p></article>
            </div>
          </div>
          <div class="trust-panel glass-card reveal-on-scroll">
            <h2>一些结果</h2>
            <div class="metric-stack">
              <div><strong>2900+</strong><span>同城商家累计获客</span></div>
              <div><strong>216 万</strong><span>GMV</span></div>
              <div><strong>20%</strong><span>自然流转化率</span></div>
            </div>
          </div>
        </div>
      </section>
    </main>
"""


CASE_DATA = {
    "yanxin": {
        "title": "杭州言心口才案例 | 钟滔",
        "description": "杭州言心口才项目案例，整理钟滔在同城新媒体获客、内容布局和线索承接上的具体工作与结果。",
        "canonical": "https://www.xn--8bx391f.com/cases/yanxin.html",
        "body": "case-page case-yanxin-page",
        "crumb": "杭州言心口才",
        "h1": "杭州言心口才",
        "subtitle": "一个偏同城获客的项目，重点不是把内容做热闹，而是把线索和承接真正接起来。",
        "meta": ["杭州 / 教育培训", "合作周期：11 个月"],
        "takeaway": [
            ("问题", "同城线索不稳定，内容和承接没有形成闭环。"),
            ("动作", "用小红书搜索、抖音自然流、信息流和私域承接一起跑。"),
            ("结果", "稳定获取精准线索，并把自然流转化率拉到 20%。"),
        ],
        "metrics": [("800+", "小红书自然流线索"), ("2100+", "抖音累计获客"), ("20%", "自然流转化率")],
        "sections": [
            ("项目背景", "杭州本地口才/演讲培训机构，希望通过新媒体扩大品牌影响力并获取稳定的同城线索。行业竞争激烈，用户决策周期长，对内容专业度和信任感要求高。"),
            ("我负责什么", "从内容定位、账号搭建、内容策略到获客路径设计与落地执行，打通从内容种草到线索收集的完整链路，并持续优化投放与自然流协同，提升整体转化效率。"),
            ("结果复盘", "通过小红书搜索布局、抖音自然流内容矩阵和信息流精准放大，持续稳定地获取同城精准线索，并通过私域承接与跟进机制，把自然流量的转化率稳步提升。"),
        ],
        "summary": {
            "项目类型": "同城获客",
            "服务范围": "内容策略 / 账号运营 / 自然流获客 / 信息流投放 / 私域承接",
            "核心方法": "小红书 SEO / 抖音自然流 / 信息流 / 同城线索",
        },
    },
    "mengli": {
        "title": "梦璃美业 IP 案例 | 钟滔",
        "description": "梦璃美业 IP 项目案例，整理钟滔在内容运营、表达调整和结果复盘上的具体工作与阶段结果。",
        "canonical": "https://www.xn--8bx391f.com/cases/mengli.html",
        "body": "case-page case-mengli-page",
        "crumb": "梦璃美业 IP",
        "h1": "梦璃美业 IP",
        "subtitle": "一个偏内容运营的项目，重点不是做多少条内容，而是让账号表达稳定地产生结果。",
        "meta": ["美业 / IP 内容运营", "合作周期：6 个月"],
        "takeaway": [
            ("问题", "账号表达不稳定，内容看完后难以继续转化。"),
            ("动作", "围绕用户问题拆选题，用数据反馈持续调整表达。"),
            ("结果", "账号反馈变稳，累计获客和 GMV 能持续落到结果上。"),
        ],
        "metrics": [("1200+", "累计获客"), ("120 万", "6 个月 GMV"), ("30%", "完播率提升")],
        "sections": [
            ("项目背景", "这类项目更偏 IP 内容运营，难点不在于有没有内容可发，而在于账号表达是不是稳定、用户是不是愿意继续看、内容最后能不能落到结果上。"),
            ("我负责什么", "围绕用户常见问题拆选题，结合数据反馈调整表达方式，并在内容节奏上持续复盘，不只看单条内容，而是看整个账号阶段性的表现是否变稳。"),
            ("结果复盘", "账号逐步形成更稳定的反馈，不再靠个别内容偶尔撑一下。完播率提升说明表达变得更顺，累计获客和 GMV 则说明内容真正被转化成了结果。"),
        ],
        "summary": {
            "项目类型": "IP 内容运营",
            "服务范围": "选题拆解 / 内容表达 / 数据复盘 / 获客转化 / 节奏优化",
            "核心方法": "内容运营 / IP 打造 / 数据反馈 / 转化复盘",
        },
    },
}


def case_main(key: str) -> str:
    data = CASE_DATA[key]
    author_focus = "内容获客 / 线索承接 / 转化复盘" if key == "yanxin" else "内容表达 / 数据复盘 / 获客转化"
    takeaway = "\n".join(
        f'                <article><strong>{name}</strong><span>{text}</span></article>' for name, text in data["takeaway"]
    )
    metrics = "\n".join(
        f'              <article><strong>{value}</strong><span>{label}</span></article>' for value, label in data["metrics"]
    )
    sections = "\n".join(
        f'            <section><h2>{heading}</h2><p>{copy}</p></section>' for heading, copy in data["sections"]
    )
    summary = "\n".join(
        f'              <div><dt>{term}</dt><dd>{value}</dd></div>' for term, value in data["summary"].items()
    )
    return f"""    <main id="main-content">
      <section class="case-hero {key}-hero" aria-label="{data["title"].split(" | ")[0]}">
        <div class="hero-bg" aria-hidden="true"></div>
        <div class="shell case-hero-grid">
          <div class="case-intro reveal-on-scroll">
            <p class="breadcrumbs"><a href="../index.html">首页</a> / 案例 / {data["crumb"]}</p>
            <h1>{data["h1"]}</h1>
            <p class="page-subtitle">{data["subtitle"]}</p>
            <div class="case-meta"><span>{data["meta"][0]}</span><span>{data["meta"][1]}</span></div>
            <div class="identity-chip case-author-chip" aria-label="项目负责人与工作重点">
              <img src="../assets/brand/portrait-zt-square.webp" alt="钟滔头像" loading="eager" decoding="async" />
              <div><span>钟滔负责</span><strong>{author_focus}</strong></div>
            </div>
            <div class="case-takeaway glass-panel">
{takeaway}
            </div>
          </div>

          <aside class="result-panel glass-card reveal-on-scroll" aria-label="关键结果">
            <h2>关键结果</h2>
            <div class="metric-stack">
{metrics}
            </div>
          </aside>
        </div>
      </section>

      <section class="section case-content" aria-label="案例正文">
        <div class="shell content-grid">
          <article class="case-text glass-panel reveal-on-scroll">
{sections}
          </article>
          <aside class="summary-panel glass-card reveal-on-scroll">
            <h2>案例摘要</h2>
            <dl>
{summary}
            </dl>
          </aside>
        </div>
      </section>
    </main>
"""


def css_for(theme: dict) -> str:
    v = theme["vars"]
    vars_css = "\n".join(f"  --{name}: {value};" for name, value in v.items())
    return f"""@import url("assets/fonts/font-faces.css");

:root {{
{vars_css}
  --font-display: "Songti SC", "STSong", "SimSun", "FangSong", "Noto Serif SC", "Source Han Serif SC", Georgia, serif;
  --font-body: "Songti SC", "STSong", "SimSun", "Noto Serif SC", "Source Han Serif SC", "Noto Sans SC", "Microsoft YaHei", serif;
  --font-sans: "Noto Sans SC", "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
  --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
  --site-width: 1260px;
  --header-height: 78px;
  --radius: 8px;
  --radius-soft: 18px;
}}

*,
*::before,
*::after {{
  box-sizing: border-box;
}}

html {{
  scroll-behavior: smooth;
  overflow-x: clip;
}}

[id] {{
  scroll-margin-top: calc(var(--header-height) + 28px);
}}

body {{
  margin: 0;
  min-height: 100vh;
  overflow-x: clip;
  color: var(--text);
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.72;
  background:
    linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

body::before {{
  content: "";
  position: fixed;
  inset: 0;
  z-index: -3;
  background:
    linear-gradient(180deg, transparent 0%, rgba(var(--surface), 0.14) 100%),
    radial-gradient(circle at 12% 12%, rgba(var(--line), 0.08), transparent 34%),
    radial-gradient(circle at 88% 18%, rgba(var(--line), 0.07), transparent 28%);
  pointer-events: none;
}}

body::after {{
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  opacity: 0.13;
  background:
    repeating-linear-gradient(90deg, rgba(var(--line), 0.13) 0 1px, transparent 1px 9px),
    repeating-linear-gradient(0deg, rgba(var(--line), 0.09) 0 1px, transparent 1px 11px);
  mix-blend-mode: normal;
  pointer-events: none;
}}

body.nav-open {{
  overflow: hidden;
}}

body,
h1,
h2,
h3,
p,
ul,
ol,
dl,
dd {{
  margin: 0;
}}

ul,
ol {{
  padding: 0;
}}

li {{
  list-style: none;
}}

img {{
  display: block;
  max-width: 100%;
  height: auto;
}}

a {{
  color: inherit;
  text-decoration: none;
}}

button {{
  font: inherit;
}}

button,
a {{
  -webkit-tap-highlight-color: transparent;
}}

:focus-visible {{
  outline: 2px solid rgba(var(--line), 0.62);
  outline-offset: 3px;
}}

.sr-only {{
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}}

.shell {{
  width: min(100% - 80px, var(--site-width));
  margin: 0 auto;
}}

.site-header {{
  position: sticky;
  top: 0;
  z-index: 100;
  min-height: var(--header-height);
  color: var(--text);
  background: var(--nav);
  border-bottom: 1px solid rgba(var(--line), var(--lineAlpha));
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.08) inset;
  backdrop-filter: blur(24px) saturate(1.38);
  -webkit-backdrop-filter: blur(24px) saturate(1.38);
}}

.site-header.is-scrolled {{
  box-shadow:
    0 18px 46px rgba(var(--shadow), var(--shadowAlpha)),
    0 1px 0 rgba(255, 255, 255, 0.08) inset;
}}

.header-inner {{
  min-height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}}

.brand {{
  display: inline-flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}}

.brand-mark {{
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: var(--radius);
  border: 1px solid rgba(var(--line), calc(var(--lineAlpha) + 0.16));
  background:
    linear-gradient(145deg, rgba(255,255,255,0.18), rgba(255,255,255,0.03)),
    rgba(var(--surfaceStrong), 0.42);
  box-shadow:
    0 14px 34px rgba(var(--shadow), calc(var(--shadowAlpha) * 0.7)),
    inset 0 1px 0 rgba(255,255,255,0.32);
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 17px;
}}

.brand-copy {{
  display: grid;
  gap: 2px;
}}

.brand-copy strong {{
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 400;
  line-height: 1.1;
}}

.brand-copy small {{
  font-family: var(--font-body);
  color: var(--muted);
  font-size: 13px;
}}

.site-nav {{
  display: flex;
  align-items: center;
  gap: 42px;
  font-size: 15px;
  font-weight: 500;
}}

.site-nav a {{
  position: relative;
  padding: 12px 0;
}}

.site-nav a::after {{
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: 6px;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 180ms ease;
}}

.site-nav a:hover,
.site-nav a:focus-visible,
.site-nav a.is-current {{
  color: var(--accent2);
}}

.site-nav a:hover::after,
.site-nav a:focus-visible::after,
.site-nav a.is-current::after {{
  transform: scaleX(1);
}}

.menu-toggle {{
  width: 46px;
  height: 46px;
  display: none;
  place-items: center;
  gap: 5px;
  padding: 0;
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  border-radius: var(--radius);
  color: var(--text);
  background: rgba(var(--surfaceStrong), 0.58);
  cursor: pointer;
}}

.menu-toggle span:not(.sr-only) {{
  display: block;
  width: 18px;
  height: 2px;
  background: currentColor;
  transition: transform 180ms ease, opacity 180ms ease;
}}

.nav-open .menu-toggle span:nth-child(1) {{
  transform: translateY(7px) rotate(45deg);
}}

.nav-open .menu-toggle span:nth-child(2) {{
  opacity: 0;
}}

.nav-open .menu-toggle span:nth-child(3) {{
  transform: translateY(-7px) rotate(-45deg);
}}

.hero,
.page-hero,
.case-hero {{
  position: relative;
  min-height: calc(100vh - var(--header-height));
  display: grid;
  align-items: center;
  isolation: isolate;
  overflow: hidden;
  padding: 92px 0;
}}

.page-hero,
.case-hero {{
  min-height: 680px;
}}

.hero-bg {{
  position: absolute;
  inset: 0;
  z-index: -2;
  background:
    var(--scrim),
    var(--page-image) center / cover no-repeat;
  opacity: var(--imageOpacity);
}}

.hero-bg::after {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, transparent 0%, var(--bg) 100%),
    radial-gradient(circle at 30% 22%, rgba(255,255,255,0.18), transparent 24%);
}}

.home-page {{ --page-image: url("assets/glass/hero.webp"); }}
.about-page {{ --page-image: url("assets/glass/contact.webp"); }}
.contact-page {{ --page-image: url("assets/glass/contact.webp"); }}
.case-yanxin-page {{ --page-image: url("assets/glass/yanxin.webp"); }}
.case-mengli-page {{ --page-image: url("assets/glass/mengli.webp"); }}

.hero-grid,
.page-hero-grid,
.case-hero-grid {{
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.72fr);
  align-items: center;
  gap: 56px;
}}

.hero-copy,
.page-copy,
.case-intro {{
  max-width: 760px;
}}

.eyebrow,
.breadcrumbs {{
  color: var(--accent2);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
}}

.breadcrumbs {{
  margin-bottom: 22px;
  color: var(--muted);
}}

h1,
h2,
h3 {{
  font-family: var(--font-display);
  font-weight: 400;
  line-height: 1.14;
}}

h1 {{
  margin-top: 18px;
  font-size: clamp(58px, 8vw, 124px);
}}

.page-copy h1,
.case-intro h1 {{
  font-size: clamp(44px, 5vw, 82px);
}}

.hero-line,
.page-subtitle {{
  margin-top: 18px;
  color: var(--accent2);
  font-family: var(--font-sans);
  font-weight: 500;
  font-size: clamp(25px, 3vw, 40px);
  line-height: 1.32;
  text-wrap: balance;
}}

.hero-summary,
.page-copy > p:not(.breadcrumbs):not(.eyebrow):not(.page-subtitle),
.section-copy p,
.case-intro > p:not(.breadcrumbs):not(.page-subtitle),
.contact-teaser p {{
  margin-top: 22px;
  max-width: 660px;
  color: var(--muted);
  font-size: 18px;
}}

.hero-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 34px;
}}

.btn {{
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: var(--radius);
  border: 1px solid rgba(var(--line), calc(var(--lineAlpha) + 0.12));
  font-family: var(--font-body);
  font-weight: 500;
  line-height: 1.2;
  box-shadow:
    0 18px 48px rgba(var(--shadow), var(--shadowAlpha)),
    inset 0 1px 0 rgba(255,255,255,0.24);
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}}

.btn:hover,
.btn:focus-visible {{
  transform: translateY(-2px);
  border-color: rgba(var(--line), 0.42);
}}

.btn-primary {{
  color: #17110a;
  background:
    linear-gradient(135deg, var(--accent2), var(--accent)),
    rgba(var(--surfaceStrong), 0.8);
}}

.btn-ghost {{
  background: rgba(var(--surfaceStrong), 0.46);
  backdrop-filter: blur(18px) saturate(1.25);
  -webkit-backdrop-filter: blur(18px) saturate(1.25);
}}

.glass-panel,
.glass-card {{
  position: relative;
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  background:
    linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.035)),
    rgba(var(--surface), var(--surfaceAlpha));
  box-shadow:
    0 28px 72px rgba(var(--shadow), var(--shadowAlpha)),
    inset 0 1px 0 rgba(255,255,255,0.26),
    inset 0 -1px 0 rgba(255,255,255,0.06);
  backdrop-filter: blur(24px) saturate(1.34);
  -webkit-backdrop-filter: blur(24px) saturate(1.34);
  overflow: hidden;
}}

.glass-card {{
  border-radius: var(--radius);
}}

.glass-panel {{
  border-radius: var(--radius-soft);
}}

.glass-panel::before,
.glass-card::before {{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at var(--mx, 22%) var(--my, 0%), rgba(255,255,255,0.34), transparent 24%),
    linear-gradient(120deg, rgba(255,255,255,0.16), transparent 34%, rgba(255,255,255,0.05) 68%, transparent);
  opacity: 0.72;
}}

.hero-panel {{
  justify-self: end;
  width: min(100%, 430px);
  padding: 28px;
}}

.panel-portrait,
.identity-chip {{
  position: relative;
  z-index: 1;
  display: inline-grid;
  grid-template-columns: 92px minmax(0, 1fr);
  align-items: center;
  gap: 14px;
  max-width: 100%;
  margin: 18px 0 4px;
  padding: 8px 14px 8px 8px;
  border: 1px solid rgba(var(--line), calc(var(--lineAlpha) + 0.08));
  border-radius: 999px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.04)),
    rgba(var(--surfaceStrong), 0.56);
  box-shadow:
    0 18px 44px rgba(var(--shadow), calc(var(--shadowAlpha) * 0.72)),
    inset 0 1px 0 rgba(255,255,255,0.18);
  backdrop-filter: blur(18px) saturate(1.18);
  -webkit-backdrop-filter: blur(18px) saturate(1.18);
}}

.panel-portrait img,
.identity-chip img {{
  width: 92px;
  height: 92px;
  object-fit: cover;
  object-position: center 40%;
  border-radius: 999px;
}}

.panel-portrait figcaption,
.identity-chip div {{
  display: grid;
  gap: 2px;
  min-width: 0;
}}

.panel-portrait span,
.identity-chip strong {{
  color: var(--text);
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.2;
}}

.panel-portrait small,
.identity-chip span {{
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}}

.panel-portrait.compact,
.qr-panel .panel-portrait {{
  grid-template-columns: 72px minmax(0, 1fr);
  margin: 18px auto 16px;
  text-align: left;
}}

.panel-portrait.compact img,
.qr-panel .panel-portrait img {{
  width: 72px;
  height: 72px;
}}

.case-author-chip {{
  margin: 18px 0 0;
  grid-template-columns: 48px minmax(0, 1fr);
  padding: 7px 14px 7px 7px;
}}

.case-author-chip img {{
  width: 48px;
  height: 48px;
}}

.metric-stack {{
  display: grid;
  gap: 14px;
  margin-top: 20px;
}}

.metric-stack div,
.metric-stack article {{
  display: grid;
  gap: 2px;
  padding: 16px 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.metric-stack div:first-child,
.metric-stack article:first-child {{
  border-top: 0;
}}

.metric-stack strong {{
  color: var(--accent2);
  font-family: var(--font-mono);
  font-size: clamp(28px, 4vw, 42px);
  line-height: 1.1;
}}

.metric-stack span {{
  color: var(--muted);
  font-size: 14px;
}}

.section {{
  padding: 104px 0;
  position: relative;
}}

.section-head {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 28px;
  margin-bottom: 36px;
}}

.section-head .eyebrow {{
  grid-column: 1 / -1;
}}

.section-head h2,
.section-copy h2,
.teaser-panel h2,
.talk-panel h2,
.trust-panel h2,
.method-aside h2,
.result-panel h2,
.summary-panel h2 {{
  font-size: clamp(30px, 3vw, 48px);
}}

.text-link {{
  color: var(--accent2);
  font-family: var(--font-body);
  font-weight: 500;
  white-space: nowrap;
}}

.case-grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}}

.case-card {{
  min-height: 560px;
  display: grid;
  grid-template-rows: 250px 1fr;
  cursor: pointer;
  transition: transform 220ms ease, box-shadow 220ms ease;
}}

.case-card:hover {{
  transform: translateY(-6px);
}}

.card-hit {{
  position: absolute;
  inset: 0;
  z-index: 4;
}}

.case-media {{
  min-height: 250px;
  background: var(--case-image) center / cover no-repeat;
  border-bottom: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.case-taixi {{ --case-image: url("assets/glass/taixi.webp"); }}
.case-yanxin {{ --case-image: url("assets/glass/yanxin.webp"); }}
.case-mengli {{ --case-image: url("assets/glass/mengli.webp"); }}

.case-body {{
  position: relative;
  z-index: 2;
  display: grid;
  gap: 16px;
  padding: 24px;
}}

.case-tag,
.case-meta span {{
  width: fit-content;
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 4px 10px;
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  border-radius: 999px;
  color: var(--accent2);
  background: rgba(var(--surfaceStrong), 0.38);
  font-size: 13px;
  font-family: var(--font-body);
  font-weight: 500;
}}

.case-card h3 {{
  font-family: var(--font-sans);
  font-size: 27px;
  font-weight: 600;
  line-height: 1.2;
  text-wrap: balance;
}}

.case-card p,
.compact-list p,
.case-text p,
.summary-panel dd,
.status-panel span,
.qr-panel p {{
  color: var(--muted);
}}

.case-metrics {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: auto;
}}

.case-metrics div {{
  min-width: 0;
  display: grid;
  gap: 3px;
  padding: 12px 10px;
  border: 1px solid rgba(var(--line), calc(var(--lineAlpha) * 0.92));
  border-radius: var(--radius);
  background: rgba(var(--surfaceStrong), 0.34);
}}

.case-metrics strong {{
  color: var(--accent2);
  font-family: var(--font-mono);
  font-size: 18px;
  line-height: 1.2;
}}

.case-metrics span {{
  color: var(--muted);
  font-size: 12px;
  line-height: 1.35;
}}

.method-grid,
.about-grid,
.lower-grid,
.content-grid {{
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(340px, 0.55fr);
  gap: 28px;
  align-items: start;
}}

.method-list,
.compact-list {{
  display: grid;
  gap: 0;
}}

.method-list {{
  padding: 10px 26px;
}}

.method-list article,
.compact-list article {{
  display: grid;
  gap: 6px;
  padding: 22px 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.method-list article:first-child,
.compact-list article:first-child {{
  border-top: 0;
}}

.method-list span {{
  color: var(--accent2);
  font-family: var(--font-mono);
  font-weight: 600;
}}

.method-list strong,
.compact-list strong {{
  font-size: 19px;
}}

.teaser-panel {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  padding: 34px;
}}

.page-hero-grid,
.contact-grid {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(310px, 430px);
  gap: 42px;
  align-items: center;
}}

.status-panel,
.qr-panel,
.method-aside,
.result-panel,
.summary-panel,
.trust-panel,
.talk-panel {{
  padding: 28px;
}}

.status-panel {{
  display: grid;
  gap: 12px;
}}

.status-panel hr {{
  width: 100%;
  border: 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
  margin: 8px 0;
}}

.timeline-panel {{
  padding: 22px 30px;
}}

.story-timeline {{
  display: grid;
  gap: 0;
}}

.story-timeline > li {{
  position: relative;
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 18px;
  padding: 24px 0;
}}

.story-timeline > li::before {{
  content: "";
  position: absolute;
  left: 16px;
  top: 46px;
  bottom: -10px;
  width: 1px;
  background: rgba(var(--line), var(--lineAlpha));
}}

.story-timeline > li:last-child::before {{
  display: none;
}}

.story-timeline > li > span {{
  width: 18px;
  height: 18px;
  margin-top: 8px;
  border-radius: 50%;
  border: 1px solid rgba(var(--line), 0.42);
  background: var(--accent);
  box-shadow: 0 0 0 6px rgba(var(--line), 0.08);
}}

.story-timeline h2 {{
  font-family: var(--font-sans);
  font-size: 26px;
  font-weight: 600;
  line-height: 1.24;
}}

.story-timeline p {{
  margin-top: 8px;
  color: var(--muted);
}}

.story-timeline .is-current {{
  color: var(--text);
}}

.proof-list {{
  display: grid;
  gap: 8px;
  margin-top: 16px;
  color: var(--muted);
}}

.proof-list li {{
  display: block;
  width: 100%;
  padding: 0 0 0 18px;
  line-height: inherit;
  list-style: disc;
}}

.proof-list li::before {{
  display: none;
}}

.method-aside {{
  position: sticky;
  top: calc(var(--header-height) + 24px);
}}

.contact-grid {{
  grid-template-columns: minmax(0, 1fr) minmax(320px, 410px);
}}

.contact-rows {{
  display: grid;
  gap: 0;
  margin-top: 28px;
  padding: 8px 20px;
}}

.contact-rows li {{
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  padding: 16px 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.contact-rows li:first-child {{
  border-top: 0;
}}

.contact-rows span {{
  color: var(--muted);
  font-family: var(--font-body);
  font-weight: 500;
}}

.copy-chip {{
  min-height: 34px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  color: var(--text);
  background: rgba(var(--surfaceStrong), 0.48);
  font-family: var(--font-body);
  cursor: pointer;
}}

.copy-chip.is-copied {{
  color: #17110a;
  background: var(--accent2);
}}

.qr-panel {{
  text-align: center;
}}

.qr-panel h2 {{
  margin-top: 8px;
  font-size: 30px;
}}

.qr-frame {{
  margin: 22px auto;
  width: min(100%, 250px);
  padding: 14px;
  border-radius: var(--radius);
  background: #fbf8ef;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.08);
}}

.qr-frame img {{
  width: 100%;
  border-radius: 4px;
}}

.contact-lower {{
  padding-top: 0;
}}

.case-hero {{
  align-items: end;
  padding-bottom: 74px;
}}

.case-hero-grid {{
  grid-template-columns: minmax(0, 1fr) minmax(320px, 410px);
  align-items: end;
}}

.case-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}}

.case-takeaway {{
  display: grid;
  gap: 0;
  max-width: 700px;
  margin-top: 28px;
  padding: 6px 22px;
}}

.case-takeaway article {{
  display: grid;
  grid-template-columns: 64px minmax(0, 1fr);
  gap: 16px;
  padding: 15px 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.case-takeaway article:first-child {{
  border-top: 0;
}}

.case-takeaway strong {{
  color: var(--accent2);
}}

.case-takeaway span {{
  color: var(--muted);
}}

.result-panel {{
  align-self: stretch;
}}

.case-text {{
  padding: 36px;
}}

.case-text section + section {{
  margin-top: 34px;
  padding-top: 34px;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.case-text h2 {{
  font-size: 30px;
}}

.case-text p {{
  margin-top: 12px;
  font-size: 17px;
}}

.summary-panel dl {{
  display: grid;
  gap: 0;
  margin-top: 18px;
}}

.summary-panel div {{
  padding: 18px 0;
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
}}

.summary-panel div:first-child {{
  border-top: 0;
}}

.summary-panel dt {{
  color: var(--accent2);
  font-family: var(--font-body);
  font-weight: 500;
}}

.summary-panel dd {{
  margin-top: 6px;
}}

.site-footer {{
  border-top: 1px solid rgba(var(--line), var(--lineAlpha));
  background: rgba(var(--surface), 0.26);
}}

.footer-inner {{
  min-height: 92px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  color: var(--muted);
  font-size: 14px;
}}

.back-to-top {{
  position: fixed;
  right: 22px;
  bottom: 22px;
  z-index: 90;
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  border-radius: var(--radius);
  color: var(--text);
  background: rgba(var(--surfaceStrong), 0.72);
  box-shadow: 0 18px 36px rgba(var(--shadow), var(--shadowAlpha));
  opacity: 0;
  transform: translateY(10px);
  pointer-events: none;
  cursor: pointer;
  backdrop-filter: blur(18px) saturate(1.2);
  -webkit-backdrop-filter: blur(18px) saturate(1.2);
  transition: opacity 180ms ease, transform 180ms ease;
}}

.back-to-top.show {{
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}}

.toast {{
  position: fixed;
  left: 50%;
  bottom: 24px;
  z-index: 120;
  transform: translate(-50%, 14px);
  padding: 10px 14px;
  border-radius: 999px;
  color: var(--text);
  background: rgba(var(--surfaceStrong), 0.9);
  border: 1px solid rgba(var(--line), var(--lineAlpha));
  opacity: 0;
  pointer-events: none;
  transition: opacity 180ms ease, transform 180ms ease;
}}

.toast.show {{
  opacity: 1;
  transform: translate(-50%, 0);
}}

.reveal-pending {{
  opacity: 0;
  transform: translateY(18px);
}}

.reveal-pending.is-visible {{
  opacity: 1;
  transform: translateY(0);
  transition: opacity 520ms ease var(--reveal-delay, 0ms), transform 520ms ease var(--reveal-delay, 0ms);
}}

.theme-immersive .hero-bg {{
  opacity: 0.78;
  background:
    linear-gradient(90deg, rgba(7,7,7,0.98) 0%, rgba(7,7,7,0.82) 34%, rgba(7,7,7,0.34) 68%, rgba(7,7,7,0.88) 100%),
    var(--page-image) center / cover no-repeat;
}}

.theme-immersive .hero-bg::after {{
  background:
    radial-gradient(circle at 70% 34%, rgba(255,255,255,0.13), transparent 22%),
    linear-gradient(180deg, rgba(7,7,7,0.05) 0%, var(--bg) 100%);
}}

.theme-immersive .hero-grid {{
  grid-template-columns: minmax(0, 0.78fr) minmax(420px, 0.58fr);
  gap: 74px;
}}

.theme-immersive .hero-copy,
.theme-immersive .page-copy,
.theme-immersive .case-intro {{
  position: relative;
  padding-left: 22px;
}}

.theme-immersive .hero-copy::before,
.theme-immersive .page-copy::before,
.theme-immersive .case-intro::before {{
  content: "";
  position: absolute;
  left: 0;
  top: 10px;
  bottom: 10px;
  width: 1px;
  background: linear-gradient(180deg, transparent, var(--accent2), transparent);
  opacity: 0.78;
}}

.theme-immersive .hero-panel,
.theme-immersive .result-panel,
.theme-immersive .qr-panel {{
  transform: translateY(22px);
}}

.theme-immersive .case-grid {{
  grid-template-columns: minmax(0, 1.18fr) minmax(0, 0.91fr) minmax(0, 0.91fr);
}}

.theme-immersive .case-card {{
  min-height: 638px;
  grid-template-rows: 328px 1fr;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.018)),
    rgba(var(--surface), 0.5);
}}

.theme-immersive .case-media {{
  min-height: 328px;
}}

.theme-immersive .glass-panel,
.theme-immersive .glass-card {{
  border-color: rgba(var(--line), 0.2);
  box-shadow:
    0 34px 90px rgba(0,0,0,0.62),
    inset 0 1px 0 rgba(255,255,255,0.18),
    inset 0 -1px 0 rgba(255,255,255,0.04);
}}

.theme-final .site-header {{
  background:
    linear-gradient(180deg, rgba(20,15,10,0.94), rgba(14,10,7,0.82));
}}

.theme-final .hero-bg {{
  opacity: 0.56;
  background:
    linear-gradient(90deg, rgba(11,9,7,0.99) 0%, rgba(11,9,7,0.88) 38%, rgba(11,9,7,0.42) 73%, rgba(11,9,7,0.94) 100%),
    var(--page-image) center / cover no-repeat;
}}

.theme-final h1 {{
  text-shadow: 0 18px 44px rgba(0,0,0,0.38);
}}

.theme-final .hero-summary,
.theme-final .page-copy > p:not(.breadcrumbs):not(.eyebrow):not(.page-subtitle),
.theme-final .section-copy p,
.theme-final .case-intro > p:not(.breadcrumbs):not(.page-subtitle) {{
  color: rgba(255,246,230,0.78);
}}

.theme-final .glass-panel,
.theme-final .glass-card {{
  background:
    linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.03)),
    rgba(var(--surface), var(--surfaceAlpha));
  box-shadow:
    0 30px 78px rgba(0,0,0,0.52),
    inset 0 1px 0 rgba(255,255,255,0.22),
    inset 0 -1px 0 rgba(255,255,255,0.055);
}}

.theme-final .case-grid {{
  gap: 24px;
}}

.theme-final .case-card {{
  min-height: 586px;
  grid-template-rows: 276px 1fr;
}}

.theme-final .case-media {{
  min-height: 276px;
}}

.theme-final .btn-primary {{
  background:
    linear-gradient(135deg, #f0c879, #c8913d 54%, #ac7430),
    rgba(var(--surfaceStrong), 0.8);
}}

@media (prefers-reduced-motion: reduce) {{
  *,
  *::before,
  *::after {{
    scroll-behavior: auto !important;
    transition-duration: 0.001ms !important;
    animation-duration: 0.001ms !important;
  }}
}}

@media (max-width: 1080px) {{
  .theme-immersive .hero-grid,
  .theme-immersive .case-grid,
  .theme-final .case-grid {{
    grid-template-columns: 1fr;
  }}

  .theme-immersive .hero-panel,
  .theme-immersive .result-panel,
  .theme-immersive .qr-panel {{
    transform: none;
  }}

  .hero-grid,
  .page-hero-grid,
  .case-hero-grid,
  .contact-grid,
  .method-grid,
  .about-grid,
  .lower-grid,
  .content-grid {{
    grid-template-columns: 1fr;
  }}

  .hero-panel,
  .status-panel,
  .qr-panel,
  .result-panel,
  .summary-panel,
  .method-aside {{
    justify-self: stretch;
    position: relative;
    top: auto;
  }}

  .case-grid {{
    grid-template-columns: 1fr;
  }}

  .case-card {{
    min-height: auto;
    grid-template-columns: minmax(260px, 0.45fr) minmax(0, 1fr);
    grid-template-rows: auto;
  }}

  .case-media {{
    min-height: 100%;
  }}
}}

@media (max-width: 860px) {{
  :root {{
    --header-height: 68px;
  }}

  .shell {{
    width: min(100% - 32px, var(--site-width));
  }}

  .site-header {{
    min-height: var(--header-height);
  }}

  .header-inner {{
    min-height: var(--header-height);
  }}

  .brand-mark {{
    width: 42px;
    height: 42px;
    font-size: 15px;
  }}

  .brand-copy strong {{
    font-size: 20px;
  }}

  .brand-copy small {{
    font-size: 12px;
  }}

  .menu-toggle {{
    display: grid;
  }}

  .site-nav {{
    position: fixed;
    left: 16px;
    right: 16px;
    top: calc(var(--header-height) + 10px);
    display: grid;
    gap: 2px;
    padding: 12px;
    border: 1px solid rgba(var(--line), calc(var(--lineAlpha) + 0.18));
    border-radius: var(--radius);
    background:
      linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.018)),
      rgb(var(--surfaceStrong));
    box-shadow: 0 24px 70px rgba(var(--shadow), calc(var(--shadowAlpha) + 0.16));
    backdrop-filter: blur(24px) saturate(1.3);
    -webkit-backdrop-filter: blur(24px) saturate(1.3);
    transform: translateY(-8px);
    opacity: 0;
    pointer-events: none;
  }}

  .nav-open .site-nav {{
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }}

  .site-nav a {{
    padding: 13px 12px;
    border-radius: 6px;
  }}

  .site-nav a::after {{
    display: none;
  }}

  .site-nav a.is-current,
  .site-nav a:hover,
  .site-nav a:focus-visible {{
    background: rgba(var(--surface), 0.42);
  }}

  .hero,
  .page-hero,
  .case-hero {{
    min-height: auto;
    padding: 76px 0 68px;
  }}

  .hero-bg {{
    background:
      linear-gradient(180deg, rgba(var(--surfaceStrong), 0.84) 0%, rgba(var(--surfaceStrong), 0.56) 44%, var(--bg) 100%),
      var(--page-image) center top / cover no-repeat;
    opacity: calc(var(--imageOpacity) + 0.1);
  }}

  h1 {{
    font-size: clamp(48px, 15vw, 76px);
  }}

  .page-copy h1,
  .case-intro h1 {{
    font-size: clamp(38px, 12vw, 58px);
  }}

  .hero-line,
  .page-subtitle {{
    font-size: clamp(24px, 7vw, 34px);
  }}

  .hero-summary,
  .page-copy > p:not(.breadcrumbs):not(.eyebrow):not(.page-subtitle),
  .section-copy p,
  .case-intro > p:not(.breadcrumbs):not(.page-subtitle),
  .contact-teaser p {{
    font-size: 16px;
  }}

  .panel-portrait,
  .identity-chip {{
    grid-template-columns: 64px minmax(0, 1fr);
    margin-top: 16px;
    padding: 7px 12px 7px 7px;
  }}

  .panel-portrait img,
  .identity-chip img,
  .panel-portrait.compact img,
  .qr-panel .panel-portrait img {{
    width: 64px;
    height: 64px;
  }}

  .panel-portrait.compact,
  .qr-panel .panel-portrait {{
    grid-template-columns: 64px minmax(0, 1fr);
  }}

  .panel-portrait span,
  .identity-chip strong {{
    font-size: 16px;
  }}

  .section {{
    padding: 72px 0;
  }}

  .section-head {{
    grid-template-columns: 1fr;
    gap: 16px;
  }}

  .section-head h2,
  .section-copy h2,
  .teaser-panel h2,
  .talk-panel h2,
  .trust-panel h2,
  .method-aside h2,
  .result-panel h2,
  .summary-panel h2 {{
    font-size: 32px;
  }}

  .case-card {{
    grid-template-columns: 1fr;
    grid-template-rows: 220px auto;
  }}

  .case-media {{
    min-height: 220px;
  }}

  .case-body {{
    padding: 20px;
  }}

  .case-card h3 {{
    font-size: 26px;
  }}

  .case-metrics {{
    grid-template-columns: 1fr;
  }}

  .method-list {{
    padding: 6px 20px;
  }}

  .teaser-panel {{
    display: grid;
    padding: 24px;
  }}

  .status-panel,
  .qr-panel,
  .method-aside,
  .result-panel,
  .summary-panel,
  .trust-panel,
  .talk-panel,
  .case-text {{
    padding: 22px;
  }}

  .timeline-panel {{
    padding: 10px 22px;
  }}

  .story-timeline > li {{
    grid-template-columns: 24px minmax(0, 1fr);
    gap: 14px;
  }}

  .story-timeline > li::before {{
    left: 11px;
  }}

  .story-timeline h2 {{
    font-size: 23px;
  }}

  .contact-rows {{
    padding: 6px 16px;
  }}

  .contact-rows li {{
    grid-template-columns: 1fr auto;
    gap: 8px 12px;
  }}

  .contact-rows li > span {{
    grid-column: 1 / -1;
  }}

  .qr-frame {{
    width: min(100%, 226px);
  }}

  .case-takeaway {{
    padding: 6px 18px;
  }}

  .case-takeaway article {{
    grid-template-columns: 1fr;
    gap: 4px;
  }}

  .footer-inner {{
    min-height: 86px;
    display: grid;
    align-content: center;
  }}
}}

@media (max-width: 420px) {{
  .brand-copy small {{
    display: none;
  }}

  .hero-actions,
  .btn {{
    width: 100%;
  }}

  .contact-rows li {{
    grid-template-columns: 1fr;
  }}

  .copy-chip {{
    width: fit-content;
  }}
}}
"""


SITE_JS = """(function () {
  var header = document.querySelector(".site-header");
  var menuToggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  var menuLinks = nav ? Array.prototype.slice.call(nav.querySelectorAll("a")) : [];
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal-on-scroll"));
  var backToTop = document.getElementById("back-to-top");
  var toast = document.getElementById("toast");
  var mobileQuery = window.matchMedia ? window.matchMedia("(max-width: 860px)") : null;
  var ticking = false;

  function isMobileNav() {
    return mobileQuery ? mobileQuery.matches : window.innerWidth <= 860;
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function updateHeaderState() {
    var currentY = window.scrollY || window.pageYOffset || 0;
    if (header) {
      header.classList.toggle("is-scrolled", currentY > 18);
    }
    if (backToTop) {
      backToTop.classList.toggle("show", currentY > 560);
    }
  }

  function syncScrollUi() {
    updateHeaderState();
    ticking = false;
  }

  function syncMenuAccessibility() {
    if (!nav || !menuToggle) {
      return;
    }
    var isOpen = document.body.classList.contains("nav-open");
    var isMobile = isMobileNav();
    var label = menuToggle.querySelector(".sr-only");
    if (!isMobile && isOpen) {
      document.body.classList.remove("nav-open");
      isOpen = false;
    }
    menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    if (label) {
      label.textContent = isOpen ? "关闭导航" : "打开导航";
    }
    if (isMobile) {
      nav.setAttribute("aria-hidden", isOpen ? "false" : "true");
      menuLinks.forEach(function (link) {
        link.tabIndex = isOpen ? 0 : -1;
      });
    } else {
      nav.removeAttribute("aria-hidden");
      menuLinks.forEach(function (link) {
        link.removeAttribute("tabindex");
      });
    }
  }

  function closeMenu() {
    document.body.classList.remove("nav-open");
    syncMenuAccessibility();
  }

  function setupReveal() {
    if (!revealItems.length) {
      return;
    }
    if (!("IntersectionObserver" in window) || prefersReducedMotion()) {
      revealItems.forEach(function (item) {
        item.classList.add("is-visible");
      });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.01, rootMargin: "0px 0px 16% 0px" });
    revealItems.forEach(function (item, index) {
      item.style.setProperty("--reveal-delay", Math.min(index * 55, 180) + "ms");
      item.classList.add("reveal-pending");
      observer.observe(item);
    });
  }

  function setupGlassPointer() {
    var targets = Array.prototype.slice.call(document.querySelectorAll(".glass-card, .glass-panel, .btn"));
    if (prefersReducedMotion()) {
      return;
    }
    targets.forEach(function (target) {
      target.addEventListener("pointermove", function (event) {
        var rect = target.getBoundingClientRect();
        var x = ((event.clientX - rect.left) / rect.width) * 100;
        var y = ((event.clientY - rect.top) / rect.height) * 100;
        target.style.setProperty("--mx", x.toFixed(1) + "%");
        target.style.setProperty("--my", y.toFixed(1) + "%");
      });
    });
  }

  function showToast(text) {
    if (!toast) {
      return;
    }
    toast.textContent = text;
    toast.classList.add("show");
    clearTimeout(toast._tid);
    toast._tid = window.setTimeout(function () {
      toast.classList.remove("show");
    }, 1500);
  }

  function copyLabelFor(selector) {
    if (selector === "#email-text") {
      return "邮箱";
    }
    if (selector === "#phone-text") {
      return "手机号";
    }
    return "内容";
  }

  function setCopiedState(button, isSuccess, label) {
    clearTimeout(button._tid);
    button.textContent = isSuccess ? "已复制" : "失败";
    button.setAttribute("aria-label", isSuccess ? label + "已复制" : label + "复制失败");
    button.classList.toggle("is-copied", isSuccess);
    button._tid = window.setTimeout(function () {
      button.textContent = "复制";
      button.setAttribute("aria-label", "复制" + label);
      button.classList.remove("is-copied");
    }, 1500);
  }

  function copyTextFromSelector(selector, button) {
    var el = document.querySelector(selector);
    if (!el) {
      return;
    }
    var text = el.textContent.trim();
    var label = copyLabelFor(selector);

    function onSuccess() {
      showToast(label + "已复制");
      setCopiedState(button, true, label);
    }

    function onFail() {
      showToast(label + "复制失败");
      setCopiedState(button, false, label);
    }

    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand("copy") ? onSuccess() : onFail();
      } catch (error) {
        onFail();
      }
      document.body.removeChild(ta);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(fallback);
    } else {
      fallback();
    }
  }

  function onScroll() {
    if (ticking) {
      return;
    }
    ticking = true;
    window.requestAnimationFrame(syncScrollUi);
  }

  if (menuToggle && nav) {
    menuToggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open", !document.body.classList.contains("nav-open"));
      syncMenuAccessibility();
    });
  }

  document.addEventListener("click", function (event) {
    if (event.target.closest(".menu-toggle")) {
      return;
    }
    if (document.body.classList.contains("nav-open") && !event.target.closest("#site-nav")) {
      closeMenu();
      return;
    }
    var backButton = event.target.closest("#back-to-top");
    if (backButton) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? "auto" : "smooth" });
      closeMenu();
      return;
    }
    var copyButton = event.target.closest("[data-copy]");
    if (copyButton) {
      event.preventDefault();
      copyTextFromSelector(copyButton.getAttribute("data-copy"), copyButton);
      return;
    }
    if (event.target.closest(".site-nav a")) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && document.body.classList.contains("nav-open")) {
      closeMenu();
      if (menuToggle) {
        menuToggle.focus();
      }
      return;
    }
    if (event.key !== "Tab" || !document.body.classList.contains("nav-open") || !isMobileNav()) {
      return;
    }
    var focusables = [menuToggle].concat(menuLinks).filter(Boolean);
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  var year = document.getElementById("year");
  if (year) {
    year.textContent = "2025";
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () {
    syncMenuAccessibility();
    syncScrollUi();
  });
  if (mobileQuery && mobileQuery.addEventListener) {
    mobileQuery.addEventListener("change", syncMenuAccessibility);
  }

  setupReveal();
  setupGlassPointer();
  syncMenuAccessibility();
  syncScrollUi();
})();
"""


def write_site(theme_key: str) -> None:
    theme = THEMES[theme_key]
    site_dir = EXPERIMENTS / theme["folder"]
    ensure_clean_dir(site_dir)
    copy_static_assets(site_dir, theme_key)
    (site_dir / "cases").mkdir(parents=True, exist_ok=True)
    (site_dir / "style.css").write_text(css_for(theme), encoding="utf-8", newline="\n")
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


def main() -> None:
    for variant in THEMES:
        write_site(variant)
    print("Generated liquid glass experiments:")
    for variant, theme in THEMES.items():
        print(f"- {variant}: {EXPERIMENTS / theme['folder']}")


if __name__ == "__main__":
    main()
