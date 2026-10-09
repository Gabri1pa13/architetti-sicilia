#!/usr/bin/env python3
"""Insert the Google Tag Manager container (GTM-WGCXFZTP) into every HTML page.

- The <script> snippet goes right after the opening <head> tag.
- The <noscript> snippet goes right after the opening <body> tag.

Idempotent: pages that already contain the container ID are skipped.
Usage: python3 scripts/add-gtm.py
"""
import re
import sys
from pathlib import Path

GTM_ID = "GTM-WGCXFZTP"
ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "node_modules", "backup-original"}

HEAD_SNIPPET = (
    "<!-- Google Tag Manager -->\n"
    "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
    "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
    "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
    "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
    f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n"
    "<!-- End Google Tag Manager -->"
)

BODY_SNIPPET = (
    "<!-- Google Tag Manager (noscript) -->\n"
    f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
    'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
    "<!-- End Google Tag Manager (noscript) -->"
)

HEAD_RE = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)
BODY_RE = re.compile(r"<body(?:\s[^>]*)?>", re.IGNORECASE)


def process(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if GTM_ID in html:
        return "skipped"
    head = HEAD_RE.search(html)
    body = BODY_RE.search(html)
    if not head or not body or body.start() < head.end():
        return "no-head-body"
    # Insert the body snippet first so the head offsets stay valid.
    html = html[: body.end()] + "\n" + BODY_SNIPPET + "\n" + html[body.end():]
    html = html[: head.end()] + "\n" + HEAD_SNIPPET + "\n" + html[head.end():]
    path.write_text(html, encoding="utf-8")
    return "updated"


def main() -> int:
    counts = {"updated": 0, "skipped": 0, "no-head-body": 0}
    for path in sorted(ROOT.rglob("*.html")):
        if EXCLUDE_DIRS.intersection(path.relative_to(ROOT).parts):
            continue
        result = process(path)
        counts[result] += 1
        if result == "no-head-body":
            print(f"WARN: <head>/<body> not found in {path.relative_to(ROOT)}")
    print(counts)
    return 1 if counts["no-head-body"] else 0


if __name__ == "__main__":
    sys.exit(main())
