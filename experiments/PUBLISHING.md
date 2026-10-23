# Live website

The live GitHub Pages site uses these root pages:

- `index.html`: the minimal portal with two destinations.
- `accounts.html`: the historical account archive (currently 17 entries).
- `portfolio.html`: a continuous vertical reader of the 25-page PDF supplied on 2026-10-23.

`assets/portal.css` provides the shared styles. `assets/portfolio.css` styles
the continuous reader. `assets/archive.css` adapts
the preserved account archive to the same palette. Lucide SVG icons are in
`assets/ui/` (lucide-static 0.468.0, ISC license).

The current public portfolio uses `assets/portfolio/20261023/`: a byte-for-byte
copy of the user-supplied PDF and its 25 WebP page renders. The PDF was rendered
with Poppler at 1920 x 1080 and converted to WebP at quality 90. Page links and
the download link must point to the same version. Source PDF/PPTX files are
not edited. Older exports are preserved in `assets/portfolio/` for recovery.

Future account changes belong in `accounts.html`. Keep the preserved
`experiments/portfolio.html` and `write_portfolio()` in
`build_minimal_resume_experiments.py` synchronized. Do not replace the root
portal with the archived account page when running experiment generators.

`_config.yml` intentionally excludes the old personal-site pages, cases,
experiments and personal-information text from publication. Keep these
exclusions unless the user asks to restore those pages. The new root account
archive and viewer are public; the old versions remain excluded.

The Feishu link, avatar, company descriptions and copyright footer remain
removed per the user's earlier requests.
