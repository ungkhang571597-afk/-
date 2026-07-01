from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
FONTS_DIR = ROOT / "assets" / "fonts"

SANS_SOURCE = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
SERIF_SOURCE = Path(r"C:\Windows\Fonts\NotoSerifSC-VF.ttf")

FONT_TARGETS = (
    (SANS_SOURCE, 400, "noto-sans-sc-400-subset.ttf"),
    (SANS_SOURCE, 500, "noto-sans-sc-500-subset.ttf"),
    (SANS_SOURCE, 600, "noto-sans-sc-600-subset.ttf"),
    (SANS_SOURCE, 700, "noto-sans-sc-700-subset.ttf"),
    (SERIF_SOURCE, 500, "noto-serif-sc-500-subset.ttf"),
    (SERIF_SOURCE, 600, "noto-serif-sc-600-subset.ttf"),
)

TEXT_PATTERNS = (
    "*.html",
    "cases/*.html",
    "site.js",
    "experiments/*.html",
    "experiments/*.py",
    "experiments/**/*.html",
    "experiments/**/site.js",
)

SKIP_PARTS = {
    ".git",
    "__pycache__",
    "output",
    "test-results",
    ".playwright-mcp",
}

FORCED_CHARS = (
    "\u5175"
    "\u3000\u3001\u3002\uff0c\uff1f\uff01\uff1a\uff1b"
    "\u201c\u201d\u2018\u2019\uff08\uff09\u300a\u300b"
    "\u3010\u3011\u00b7\u2014\u2026\uffe5\uff05"
)


def visible_html_text(source: str) -> str:
    source = re.sub(r"<script[\s\S]*?</script>", "", source, flags=re.I)
    source = re.sub(r"<style[\s\S]*?</style>", "", source, flags=re.I)
    source = re.sub(r"<[^>]+>", " ", source)
    return html.unescape(source)


def iter_text_files() -> list[Path]:
    paths: set[Path] = set()
    for pattern in TEXT_PATTERNS:
        for path in ROOT.glob(pattern):
            if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_PARTS):
                paths.add(path)
    return sorted(paths)


def collect_codepoints() -> set[int]:
    codepoints: set[int] = set(range(0x20, 0x7F))
    codepoints.add(0x00A0)

    for char in FORCED_CHARS:
        codepoints.add(ord(char))

    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix.lower() == ".html":
            text = visible_html_text(text)
        for char in text:
            value = ord(char)
            if char.isspace():
                codepoints.add(0x20)
            elif value >= 0x80:
                codepoints.add(value)

    return codepoints


def font_codepoints(path: Path) -> set[int]:
    font = TTFont(path)
    codepoints: set[int] = set()
    for table in font["cmap"].tables:
        codepoints.update(table.cmap.keys())
    return codepoints


def write_unicodes_file(path: Path, codepoints: set[int]) -> None:
    lines = [f"U+{codepoint:04X}" for codepoint in sorted(codepoints)]
    path.write_text(",".join(lines), encoding="ascii")


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def validate_font(path: Path, weight: int, required: set[int]) -> None:
    font = TTFont(path)
    cmap = font_codepoints(path)
    missing = sorted(required - cmap)
    if missing:
        sample = ", ".join(f"U+{codepoint:04X}" for codepoint in missing[:20])
        raise RuntimeError(f"{path.name} is missing {len(missing)} codepoints: {sample}")
    if font["OS/2"].usWeightClass != weight:
        raise RuntimeError(
            f"{path.name} has weight {font['OS/2'].usWeightClass}, expected {weight}"
        )
    if "fvar" in font or "gvar" in font:
        raise RuntimeError(f"{path.name} is still a variable font")


def main() -> None:
    missing_sources = [str(source) for source, _, _ in FONT_TARGETS if not source.exists()]
    if missing_sources:
        raise FileNotFoundError("Missing source fonts: " + ", ".join(sorted(set(missing_sources))))

    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    codepoints = collect_codepoints()
    if 0x5175 not in codepoints:
        raise RuntimeError("Required codepoint U+5175 was not collected")

    with tempfile.TemporaryDirectory(prefix="zt-font-subset-") as temp_name:
        temp_dir = Path(temp_name)
        unicodes_file = temp_dir / "unicodes.txt"
        write_unicodes_file(unicodes_file, codepoints)

        built_fonts: list[tuple[Path, Path]] = []
        unsupported_by_source: dict[str, list[int]] = {}
        for source, weight, filename in FONT_TARGETS:
            source_cmap = font_codepoints(source)
            supported_codepoints = codepoints & source_cmap
            unsupported = sorted(codepoints - source_cmap)
            if unsupported:
                unsupported_by_source[source.name] = unsupported
            static_font = temp_dir / f"{Path(filename).stem}-static.ttf"
            subset_font = temp_dir / filename
            run(
                [
                    sys.executable,
                    "-m",
                    "fontTools.varLib.instancer",
                    "--static",
                    "-o",
                    str(static_font),
                    str(source),
                    f"wght={weight}",
                ]
            )
            run(
                [
                    sys.executable,
                    "-m",
                    "fontTools.subset",
                    str(static_font),
                    f"--unicodes-file={unicodes_file}",
                    "--layout-features=*",
                    "--name-IDs=*",
                    "--name-languages=*",
                    "--notdef-glyph",
                    "--recommended-glyphs",
                    f"--output-file={subset_font}",
                ]
            )
            validate_font(subset_font, weight, supported_codepoints)
            built_fonts.append((subset_font, FONTS_DIR / filename))

        for source, destination in built_fonts:
            shutil.copy2(source, destination)

    print(f"Rebuilt {len(FONT_TARGETS)} Noto subsets with {len(codepoints)} codepoints.")
    print("U+5175 included: yes")
    for source_name, unsupported in sorted(unsupported_by_source.items()):
        sample = ", ".join(f"U+{codepoint:04X}" for codepoint in unsupported[:12])
        print(f"{source_name} unsupported codepoints ignored: {len(unsupported)} ({sample})")


if __name__ == "__main__":
    main()
