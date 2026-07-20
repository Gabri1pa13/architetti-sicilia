#!/usr/bin/env python3
"""Replace the uniform, bulk-regenerated <lastmod> in sitemap.xml with each
URL's real last-modified date, taken from git history of the matching file.

The SEO audit flagged that every one of the 827 sitemap URLs shared the
exact same lastmod timestamp, which reads to Google as generated, not
reflective of real per-page changes. Run this after content changes and
before publishing an updated sitemap.

Usage:
    python3 scripts/fix-sitemap-lastmod.py
"""
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"


def url_to_relpath(url: str) -> str:
    path = urlparse(url).path.lstrip("/")
    if path == "" or path.endswith("/"):
        path = path + "index.html"
    return path


def build_last_commit_dates() -> dict[str, str]:
    """Map every tracked file to the date of its most recent commit."""
    output = subprocess.run(
        ["git", "log", "--diff-filter=AM", "--name-only", "--format=COMMIT %ad", "--date=short"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout

    dates: dict[str, str] = {}
    current_date = None
    for line in output.splitlines():
        if line.startswith("COMMIT "):
            current_date = line[len("COMMIT "):].strip()
        elif line.strip():
            dates.setdefault(line.strip(), current_date)
    return dates


def main() -> None:
    dates = build_last_commit_dates()
    xml = SITEMAP_PATH.read_text(encoding="utf-8")

    missing = []

    def replace_block(match: re.Match) -> str:
        block = match.group(0)
        url = re.search(r"<loc>(.*?)</loc>", block).group(1)
        relpath = url_to_relpath(url)
        date = dates.get(relpath)
        if date is None:
            missing.append(relpath)
            return block
        return re.sub(r"<lastmod>.*?</lastmod>", f"<lastmod>{date}</lastmod>", block)

    new_xml = re.sub(r"<url>.*?</url>", replace_block, xml, flags=re.DOTALL)
    SITEMAP_PATH.write_text(new_xml, encoding="utf-8")

    print(f"Updated lastmod for {xml.count('<url>') - len(missing)} URLs")
    if missing:
        print(f"No git history found for {len(missing)} paths (left unchanged), e.g.: {missing[:5]}")


if __name__ == "__main__":
    main()
