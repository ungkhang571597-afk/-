# Live website

The live GitHub Pages site uses these root pages:

- `index.html`: the minimal portal with two destinations.
- `accounts.html`: the historical account archive (currently 17 entries).
- `portfolio.html`: a continuous vertical reader of the 20-page PowerPoint export.

`assets/portal.css` provides the shared styles. `assets/portfolio.css` styles
the continuous reader. `assets/archive.css` adapts
the preserved account archive to the same palette. Lucide SVG icons are in
`assets/ui/` (lucide-static 0.468.0, ISC license).

The original PPTX was read-only exported through PowerPoint. The source file
was not changed. `assets/portfolio/` contains the PDF and WebP slide exports.
Do not overwrite these with a regenerated presentation.

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
