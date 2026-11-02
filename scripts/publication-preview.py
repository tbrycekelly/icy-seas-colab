#!/usr/bin/env python3
"""Render a publication preview using Poppler and Pillow.

Usage: python3 scripts/publication-preview.py 2024lowin /path/to/article.pdf
Use --page 2 when a repository PDF has a cover sheet before the article.
Requires pdftoppm (brew install poppler) and Pillow (python3 -m pip install Pillow).
PDFs stay outside the published site; only the optimized WebP is saved.
"""

import argparse
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("publication", help="Publication filename without .md")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]{4}[a-z0-9-]+", args.publication):
        parser.error("Use a publication identifier such as 2024lowin")
    if args.page < 1 or not args.pdf.read_bytes().startswith(b"%PDF"):
        parser.error("Supply a PDF and a positive page number")
    root = Path(__file__).resolve().parents[1]
    content = root / "content/publication" / f"{args.publication}.md"
    text = content.read_text()
    metadata = tomllib.loads(text.split("+++", 2)[1])
    if "image_preview" not in metadata:
        parser.error("The publication must have an image_preview field")
    output = root / "static/publications/previews" / f"{args.publication}.webp"
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        prefix = Path(temporary) / "page"
        subprocess.run([
            "pdftoppm", "-f", str(args.page), "-l", str(args.page),
            "-singlefile", "-scale-to", "900", "-png", str(args.pdf), str(prefix),
        ], check=True)
        with Image.open(prefix.with_suffix(".png")) as original:
            image = original.convert("RGB")
        image.thumbnail((480, 640), Image.Resampling.LANCZOS)
        preview = Image.new("RGB", (480, 640), "white")
        preview.paste(image, ((480 - image.width) // 2, (640 - image.height) // 2))
        preview.save(output, "WEBP", quality=85, method=6)
    frontmatter, body = text.split("+++", 2)[1:]
    frontmatter = re.sub(r'^image_preview\s*=.*$',
                        f'image_preview = "/publications/previews/{output.name}"',
                        frontmatter, count=1, flags=re.MULTILINE)
    content.write_text("+++" + frontmatter + "+++" + body)
    print(f"Updated {content.relative_to(root)} and {output.relative_to(root)}")


if __name__ == "__main__":
    main()
