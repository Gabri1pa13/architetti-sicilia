#!/usr/bin/env python3
"""Notify Bing/Yandex via IndexNow that all URLs in sitemap.xml may have changed.

Usage:
    python3 scripts/indexnow-ping.py

Requires no dependencies beyond the standard library. The IndexNow key is
public by design (it just proves control of the host via the key file at
the domain root), so no secrets are needed to run this.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOST = "architettisicilia.it"
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def find_key_file() -> str:
    matches = list(REPO_ROOT.glob("*.txt"))
    for path in matches:
        if re.fullmatch(r"[a-f0-9]{32}\.txt", path.name):
            return path.stem
    raise SystemExit("IndexNow key file (32-hex-char .txt) not found at repo root")


def load_sitemap_urls() -> list[str]:
    xml = SITEMAP_PATH.read_text(encoding="utf-8")
    return re.findall(r"<loc>(.*?)</loc>", xml)


def main() -> None:
    key = find_key_file()
    urls = load_sitemap_urls()
    if not urls:
        raise SystemExit("No URLs found in sitemap.xml")

    payload = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }).encode("utf-8")

    request = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(f"IndexNow: submitted {len(urls)} URLs, status {response.status}")
    except urllib.error.HTTPError as exc:
        print(f"IndexNow: submission failed, status {exc.code}: {exc.read().decode(errors='replace')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
