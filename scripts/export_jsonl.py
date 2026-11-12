#!/usr/bin/env python3
"""
Export backed-up CNCF Graduated documentation into a JSON Lines (.jsonl) file
ready for embedding / RAG ingestion.

Each JSONL record includes:
  - id           : stable "<project_slug>:<relative_path>"
  - layer        : CNCF architectural layer (e.g., "Orchestration & Core")
  - layer_slug   : directory slug (e.g., "orchestration-core")
  - project      : project display name
  - project_slug : project slug
  - title        : extracted from YAML/TOML frontmatter or first Markdown/RST heading
  - format       : "markdown" | "rst" | "code"
  - local_path   : repo-relative file path
  - upstream_url : canonical GitHub blob URL pinned to the exact synced commit SHA
  - commit_sha   : upstream git commit SHA
  - content      : UTF-8 text content

Usage:
  python3 scripts/export_jsonl.py --output corpus.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCK_MANIFEST = REPO_ROOT / "manifest" / "lock.json"

PROSE_EXTS = {".md", ".mdx", ".rst", ".txt"}
CODE_EXTS = {
    ".yaml", ".yml", ".json", ".toml", ".hcl", ".rego", ".proto",
    ".sh", ".bash", ".py", ".go", ".js", ".ts", ".conf", ".ini",
    ".cfg", ".xml", ".sql", ".promql", ".graphql",
}


def extract_title(text: str, ext: str, fallback: str) -> str:
    # Check YAML frontmatter (--- ... ---) or TOML frontmatter (+++ ... +++)
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            fm = text[4:end]
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.M)
            if m:
                return m.group(1).strip()
    elif text.startswith("+++\n"):
        end = text.find("\n+++", 4)
        if end != -1:
            fm = text[4:end]
            m = re.search(r'^title\s*=\s*["\'](.+?)["\']\s*$', fm, re.M)
            if m:
                return m.group(1).strip()

    if ext in (".md", ".mdx"):
        m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
        if m:
            return m.group(1).strip()
    elif ext == ".rst":
        lines = text.splitlines()
        for i in range(len(lines) - 1):
            title_line = lines[i].strip()
            underline = lines[i + 1].strip()
            if (
                title_line
                and len(underline) >= len(title_line)
                and len(set(underline)) == 1
                and underline[0] in "=-~^#*+"
            ):
                return title_line
    return fallback


def resolve_upstream_blob(project_rec: dict[str, Any], rel_to_project: str) -> tuple[str, str]:
    """Map a file inside docs/<layer>/<project>/ back to (upstream_blob_url, commit_sha)."""
    best_match = None
    best_prefix_len = -1

    for src in project_rec["sources"]:
        for mapping in src["mappings"]:
            local_sub = mapping["local_subdir"]
            if local_sub == ".":
                sub_rel = rel_to_project
                pfx_len = 0
            elif rel_to_project == local_sub or rel_to_project.startswith(local_sub + "/"):
                sub_rel = rel_to_project[len(local_sub):].lstrip("/")
                pfx_len = len(local_sub)
            else:
                continue

            if pfx_len > best_prefix_len:
                best_prefix_len = pfx_len
                up_base = mapping["upstream_path"].strip("/")
                up_path = f"{up_base}/{sub_rel}".strip("/") if up_base else sub_rel
                url = f"https://github.com/{src['repo']}/blob/{src['commit_sha']}/{up_path}"
                best_match = (url, src["commit_sha"])

    if best_match:
        return best_match
    first = project_rec["sources"][0]
    return (f"https://github.com/{first['repo']}/tree/{first['commit_sha']}", first["commit_sha"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Export CNCF docs backup to JSONL for RAG.")
    parser.add_argument(
        "--output",
        "-o",
        default="corpus.jsonl",
        help="Output JSONL file path (default: corpus.jsonl)",
    )
    parser.add_argument(
        "--include-code",
        action="store_true",
        help="Also include standalone YAML/JSON/code example files (default: prose .md/.mdx/.rst/.txt only).",
    )
    args = parser.parse_args()

    lock = json.loads(LOCK_MANIFEST.read_text(encoding="utf-8"))
    allowed = set(PROSE_EXTS) | (CODE_EXTS if args.include_code else set())

    out_path = Path(args.output)
    written = 0

    with out_path.open("w", encoding="utf-8") as out_f:
        for proj in lock["projects"]:
            proj_dir = REPO_ROOT / proj["local_path"]
            if not proj_dir.is_dir():
                continue

            for file_path in sorted(proj_dir.rglob("*")):
                if not file_path.is_file():
                    continue
                ext = file_path.suffix.lower()
                if ext not in allowed:
                    continue

                content = file_path.read_text(encoding="utf-8", errors="replace").strip()
                if not content:
                    continue

                rel_to_proj = file_path.relative_to(proj_dir).as_posix()
                rel_to_repo = file_path.relative_to(REPO_ROOT).as_posix()
                upstream_url, sha = resolve_upstream_blob(proj, rel_to_proj)
                fmt = "rst" if ext == ".rst" else ("markdown" if ext in (".md", ".mdx", ".txt") else "code")
                title = extract_title(content, ext, file_path.stem)

                record = {
                    "id": f"{proj['slug']}:{rel_to_proj}",
                    "layer": proj["layer"],
                    "layer_slug": proj["layer_slug"],
                    "project": proj["name"],
                    "project_slug": proj["slug"],
                    "title": title,
                    "format": fmt,
                    "local_path": rel_to_repo,
                    "upstream_url": upstream_url,
                    "commit_sha": sha,
                    "content": content,
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                written += 1

    print(f"Exported {written:,} documents to {out_path} ({out_path.stat().st_size / 1_000_000:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
