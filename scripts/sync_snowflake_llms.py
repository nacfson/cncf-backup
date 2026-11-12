#!/usr/bin/env python3
"""
Fetch Snowflake's core documentation from https://docs.snowflake.com/llms.txt
using Snowflake's native Markdown endpoints (`https://docs.snowflake.com/en/.../*.md`).

Why a separate script?
  Snowflake's main product & SQL reference (`docs.snowflake.com`) is not hosted in
  a public GitHub repository; instead, Snowflake publishes a hierarchical
  `llms.txt` index where every documentation page is available directly as `.md`.
  Run this script on any machine with direct HTTPS access to `docs.snowflake.com`
  to populate `docs/data-lakehouse/snowflake/reference-site/`.

Usage:
  # Fetch all sections indexed under https://docs.snowflake.com/llms.txt
  python3 scripts/sync_snowflake_llms.py

  # Fetch only specific path prefixes (e.g., SQL reference and Cortex AI guides)
  python3 scripts/sync_snowflake_llms.py --section sql-reference --section user-guide/snowflake-cortex

  # Limit total pages during a quick test
  python3 scripts/sync_snowflake_llms.py --limit 100
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "docs" / "data-lakehouse" / "snowflake" / "reference-site"
ROOT_LLMS_URL = "https://docs.snowflake.com/llms.txt"
USER_AGENT = "cncf-apache-docs-backup/1.0 (+https://github.com/nacfson/cncf-backup)"

LINK_RE = re.compile(r"https?://docs\.snowflake\.com/[^\s)\]>\"']+")


def fetch_text(url: str, retries: int = 3, timeout: float = 20.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/markdown, text/plain, */*"})
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code in (403, 404):
                break
            time.sleep(0.5 * (2 ** attempt))
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def to_markdown_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path.rstrip("/")
    if not path:
        path = "/en/index"
    if not path.endswith((".md", ".txt")):
        path = f"{path}.md"
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def discover_markdown_urls(root_url: str, sections: list[str] | None) -> list[str]:
    print(f"Fetching root index: {root_url}")
    root_txt = fetch_text(root_url)
    found_urls = list(dict.fromkeys(LINK_RE.findall(root_txt)))

    sub_indexes = [u for u in found_urls if u.endswith("llms.txt") and u != root_url]
    page_urls: list[str] = [u for u in found_urls if not u.endswith("llms.txt")]

    for idx_url in sub_indexes:
        try:
            sub_txt = fetch_text(idx_url)
            for link in LINK_RE.findall(sub_txt):
                if not link.endswith("llms.txt"):
                    page_urls.append(link)
        except RuntimeError as err:
            print(f"  [WARN] Skipping sub-index {idx_url}: {err}", file=sys.stderr)

    md_urls: list[str] = []
    seen: set[str] = set()
    for raw in page_urls:
        md_u = to_markdown_url(raw)
        if sections:
            rel = urllib.parse.urlsplit(md_u).path.lstrip("/")
            if rel.startswith("en/"):
                rel = rel[3:]
            if not any(rel.startswith(s.strip("/")) for s in sections):
                continue
        if md_u not in seen:
            seen.add(md_u)
            md_urls.append(md_u)

    return md_urls


def download_one(md_url: str, dest_root: Path) -> tuple[str, int, str | None]:
    parsed = urllib.parse.urlsplit(md_url)
    rel_path = parsed.path.lstrip("/")
    if rel_path.startswith("en/"):
        rel_path = rel_path[3:]
    out_file = dest_root / rel_path
    try:
        content = fetch_text(md_url)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8")
        out_file.write_bytes(data)
        return (rel_path, len(data), None)
    except RuntimeError as err:
        return (rel_path, 0, str(err))


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs.snowflake.com Markdown pages via llms.txt.")
    parser.add_argument(
        "--dest",
        default=str(DEFAULT_DEST),
        help=f"Destination directory (default: {DEFAULT_DEST.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--section",
        action="append",
        dest="sections",
        help="Optional path prefix filter under /en/ (e.g. sql-reference, developer-guide, user-guide/snowflake-cortex).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of pages to download.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Concurrent download workers (default: 6).",
    )
    args = parser.parse_args()

    dest_root = Path(args.dest)
    dest_root.mkdir(parents=True, exist_ok=True)

    try:
        urls = discover_markdown_urls(ROOT_LLMS_URL, args.sections)
    except RuntimeError as err:
        print(
            f"Error accessing {ROOT_LLMS_URL}: {err}\n"
            "Note: Run this script from an environment with direct HTTPS access to docs.snowflake.com.",
            file=sys.stderr,
        )
        return 1

    if args.limit is not None:
        urls = urls[: args.limit]

    print(f"Downloading {len(urls):,} Snowflake Markdown pages to {dest_root} (workers={args.workers})...")
    ok_count = 0
    total_bytes = 0
    failures = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for rel_path, nbytes, err in pool.map(lambda u: download_one(u, dest_root), urls):
            if err is None:
                ok_count += 1
                total_bytes += nbytes
            else:
                failures += 1

    meta_file = dest_root / "_sync_metadata.json"
    meta_file.write_text(
        json.dumps(
            {
                "source": ROOT_LLMS_URL,
                "synced_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "sections_filter": args.sections,
                "pages_downloaded": ok_count,
                "pages_failed": failures,
                "total_bytes": total_bytes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"Completed! Downloaded {ok_count:,} pages ({total_bytes / 1_000_000:.2f} MB), "
        f"{failures} skipped/failed -> {dest_root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
