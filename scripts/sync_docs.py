#!/usr/bin/env python3
"""
Synchronize CNCF Graduated Project documentation into docs/<layer>/<project>/.

Features:
- Uses `git clone --depth 1 --filter=blob:none --sparse` so monorepos (Cilium,
  Envoy, Rook, OPA, containerd) and large Hugo sites (Kubernetes, Istio) only
  transfer the exact documentation blobs needed.
- Dynamically resolves latest documentation versions for multi-version repos
  (etcd, Linkerd, Jaeger) so future re-syncs automatically pick up new releases.
- Supports three scopes:
    * text-svg   (default): Markdown/RST/text + code/config examples + SVG diagrams
    * text-only  : Markdown/RST/text + code/config examples only
    * all-media  : Includes PNG/JPG/GIF/WebP/PDF/MP4 assets as well
- Writes `manifest/lock.json` (commit SHAs, timestamps, resolved paths, counts,
  sizes) and regenerates `README.md` with a complete inventory table.

Zero third-party Python dependencies required (Python 3.9+ stdlib + `git`).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_MANIFEST = REPO_ROOT / "manifest" / "projects.json"
LOCK_MANIFEST = REPO_ROOT / "manifest" / "lock.json"
DOCS_ROOT = REPO_ROOT / "docs"
README_PATH = REPO_ROOT / "README.md"

MAX_FILE_BYTES = 45 * 1024 * 1024  # Stay safely below GitHub's 50 MB warning / 100 MB hard limit
MAX_SVG_BYTES = 1_000_000          # Skip multi-MB base64-raster-embedded .drawio.svg dumps in text-svg mode

DOC_EXTS = {".md", ".mdx", ".rst", ".txt"}
CODE_CONFIG_EXTS = {
    ".yaml", ".yml", ".json", ".toml", ".hcl", ".rego", ".proto",
    ".sh", ".bash", ".py", ".go", ".js", ".ts", ".conf", ".ini",
    ".cfg", ".xml", ".sql", ".promql", ".graphql",
}
SVG_EXTS = {".svg"}
RASTER_VIDEO_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".pdf", ".mp4", ".webm", ".mov", ".drawio",
}

BINARY_SPARSE_EXCLUDES = [
    "!**/*.png", "!**/*.PNG",
    "!**/*.jpg", "!**/*.JPG",
    "!**/*.jpeg", "!**/*.JPEG",
    "!**/*.gif", "!**/*.GIF",
    "!**/*.webp", "!**/*.WEBP",
    "!**/*.ico",
    "!**/*.pdf", "!**/*.PDF",
    "!**/*.mp4", "!**/*.MP4",
    "!**/*.webm", "!**/*.mov",
    "!**/*.pptx", "!**/*.drawio", "!**/*.graffle",
    "!**/*.woff", "!**/*.woff2", "!**/*.ttf", "!**/*.eot",
    "!**/*.zip", "!**/*.tar.gz", "!**/*.tgz",
]


def run_git(args: list[str], cwd: Path | None = None) -> str:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    res = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed (code {res.returncode}): {res.stderr.strip()}"
        )
    return res.stdout


def semver_sort_key(name: str) -> tuple[int, ...]:
    nums = [int(x) for x in re.findall(r"\d+", name)]
    return tuple(nums) if nums else (0,)


def list_tree_dirs(clone_dir: Path, parent_dir: str) -> list[str]:
    target = f"HEAD:{parent_dir}" if parent_dir else "HEAD"
    out = run_git(["ls-tree", "-d", "--name-only", target], cwd=clone_dir)
    return [line.strip() for line in out.splitlines() if line.strip()]


def path_exists_in_tree(clone_dir: Path, rel_path: str) -> bool:
    rel_path = rel_path.strip("/")
    if not rel_path:
        return True
    res = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{rel_path}"],
        cwd=str(clone_dir),
        capture_output=True,
    )
    return res.returncode == 0


def resolve_dynamic_path(clone_dir: Path, resolver: dict[str, Any]) -> tuple[str, str]:
    """Return (resolved_version, resolved_path)."""
    rtype = resolver["type"]
    if rtype == "yaml_key":
        cfg_file = resolver["config_file"]
        run_git(["sparse-checkout", "set", "--no-cone", f"/{cfg_file}"], cwd=clone_dir)
        cfg_path = clone_dir / cfg_file
        if cfg_path.is_file():
            content = cfg_path.read_text(encoding="utf-8", errors="replace")
            m = re.search(resolver["regex"], content)
            if m:
                ver = m.group(1)
                candidate = resolver["path_template"].format(version=ver)
                if path_exists_in_tree(clone_dir, candidate):
                    return ver, candidate

        # Fallback to highest semver directory
        parent = resolver["fallback_parent"]
        pat = re.compile(resolver["fallback_regex"])
        dirs = [d for d in list_tree_dirs(clone_dir, parent) if pat.match(d)]
        if not dirs:
            raise RuntimeError(f"Could not resolve version directory under {parent}")
        best = sorted(dirs, key=semver_sort_key)[-1]
        return best, resolver["path_template"].format(version=best)

    if rtype == "highest_semver_dir":
        parent = resolver["parent_dir"]
        pat = re.compile(resolver["regex"])
        dirs = [d for d in list_tree_dirs(clone_dir, parent) if pat.match(d)]
        if not dirs:
            raise RuntimeError(f"No matching version directories under {parent}")
        best = sorted(dirs, key=semver_sort_key)[-1]
        return best, resolver["path_template"].format(version=best)

    raise ValueError(f"Unknown version_resolver type: {rtype}")


def allowed_extensions(scope: str, svg_only: bool = False) -> set[str]:
    if svg_only:
        return set() if scope == "text-only" else set(SVG_EXTS)
    allowed = DOC_EXTS | CODE_CONFIG_EXTS
    if scope in ("text-svg", "all-media"):
        allowed |= SVG_EXTS
    if scope == "all-media":
        allowed |= RASTER_VIDEO_EXTS
    return allowed


def build_sparse_patterns(
    resolved_paths: list[dict[str, Any]],
    exclude_dirs: set[str],
    scope: str,
) -> list[str]:
    patterns: list[str] = [
        "/LICENSE*",
        "/LICENCE*",
        "/NOTICE*",
        "/COPYING*",
    ]
    for p in resolved_paths:
        src = p["src"].strip("/")
        svg_only = p.get("svg_only", False)
        if svg_only:
            if scope == "text-only":
                continue
            if src:
                patterns.extend([
                    f"/{src}/*.svg", f"/{src}/**/*.svg",
                    f"/{src}/*.SVG", f"/{src}/**/*.SVG",
                ])
            else:
                patterns.extend(["/*.svg", "/**/*.svg", "/*.SVG", "/**/*.SVG"])
        else:
            if src:
                patterns.extend([f"/{src}/*", f"/{src}/**"])
                for ex in sorted(exclude_dirs):
                    patterns.append(f"!/{src}/{ex}/**")
            else:
                patterns.extend(["/*", "/**"])
                for ex in sorted(exclude_dirs):
                    patterns.append(f"!/{ex}/**")

    if scope == "text-only":
        patterns.extend(BINARY_SPARSE_EXCLUDES)
        patterns.extend(["!**/*.svg", "!**/*.SVG"])
    elif scope == "text-svg":
        patterns.extend(BINARY_SPARSE_EXCLUDES)

    return patterns


def copy_filtered_tree(
    src_root: Path,
    dest_root: Path,
    allowed_exts: set[str],
    exclude_dirs: set[str],
    exclude_files: set[str],
    clone_root: Path,
) -> dict[str, int]:
    stats = {
        "markdown": 0,
        "rst": 0,
        "text_other": 0,
        "code_config": 0,
        "svg": 0,
        "media_other": 0,
        "total_files": 0,
        "total_bytes": 0,
        "skipped_symlinks": 0,
        "skipped_oversize": 0,
    }
    if not allowed_exts or not src_root.exists():
        return stats

    clone_root_real = clone_root.resolve()

    for dirpath, dirnames, filenames in os.walk(src_root, followlinks=False):
        # Prune excluded directories and directory symlinks in-place
        kept_dirs = []
        for d in sorted(dirnames):
            if d in exclude_dirs or d.startswith(".git"):
                continue
            full_d = Path(dirpath) / d
            if full_d.is_symlink():
                stats["skipped_symlinks"] += 1
                continue
            kept_dirs.append(d)
        dirnames[:] = kept_dirs

        rel_dir = Path(dirpath).relative_to(src_root)
        for fname in sorted(filenames):
            if fname in exclude_files or fname.lower().endswith(".min.js"):
                continue
            # Skip root license files here; licenses are copied explicitly
            if rel_dir == Path(".") and re.match(r"^(LICENSE|LICENCE|NOTICE|COPYING)(\..+)?$", fname, re.I):
                continue

            src_file = Path(dirpath) / fname
            if src_file.is_symlink():
                try:
                    resolved = src_file.resolve(strict=True)
                    resolved.relative_to(clone_root_real)
                    if not resolved.is_file():
                        stats["skipped_symlinks"] += 1
                        continue
                    src_to_read = resolved
                except (OSError, ValueError):
                    stats["skipped_symlinks"] += 1
                    continue
            else:
                if not src_file.is_file():
                    continue
                src_to_read = src_file

            ext = src_file.suffix.lower()
            if ext not in allowed_exts:
                continue

            size = src_to_read.stat().st_size
            if size > MAX_FILE_BYTES or (ext in SVG_EXTS and ".png" not in allowed_exts and size > MAX_SVG_BYTES):
                stats["skipped_oversize"] += 1
                continue

            out_file = dest_root / rel_dir / fname
            out_file.parent.mkdir(parents=True, exist_ok=True)
            if ext in (DOC_EXTS | CODE_CONFIG_EXTS):
                raw_bytes = src_to_read.read_bytes()
                text_data = raw_bytes.decode("utf-8", errors="surrogateescape")
                sanitized = re.sub(
                    r"xox([baprs])-[0-9]{8,}-[0-9A-Za-z-]{10,}",
                    r"xox\1-EXAMPLE-REDACTED-DOC-TOKEN",
                    text_data,
                )
                sanitized = re.sub(
                    r"\bgh([pousr])_[A-Za-z0-9]{36,}\b",
                    r"gh\1_EXAMPLE_REDACTED_DOC_TOKEN",
                    sanitized,
                )
                if sanitized != text_data:
                    out_bytes = sanitized.encode("utf-8", errors="surrogateescape")
                    out_file.write_bytes(out_bytes)
                    size = len(out_bytes)
                else:
                    shutil.copyfile(src_to_read, out_file)
            else:
                shutil.copyfile(src_to_read, out_file)

            stats["total_files"] += 1
            stats["total_bytes"] += size
            if ext in (".md", ".mdx"):
                stats["markdown"] += 1
            elif ext == ".rst":
                stats["rst"] += 1
            elif ext == ".txt":
                stats["text_other"] += 1
            elif ext in CODE_CONFIG_EXTS:
                stats["code_config"] += 1
            elif ext in SVG_EXTS:
                stats["svg"] += 1
            else:
                stats["media_other"] += 1

    return stats


def copy_upstream_license(clone_dir: Path, project_dest: Path, license_dest: str) -> str | None:
    candidates = sorted(
        p for p in clone_dir.iterdir()
        if p.is_file() and not p.is_symlink()
        and re.match(r"^(LICENSE|LICENCE|COPYING)(\..+)?$", p.name, re.I)
    )
    if not candidates:
        return None
    target = project_dest / license_dest
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(candidates[0], target)
    return license_dest


def sync_project(project: dict[str, Any], scope: str, tmp_base: Path) -> dict[str, Any]:
    slug = project["slug"]
    layer_slug = project["layer_slug"]
    project_dest = DOCS_ROOT / layer_slug / slug

    # Clean existing destination directory for idempotent sync
    if project_dest.exists():
        shutil.rmtree(project_dest)
    project_dest.mkdir(parents=True, exist_ok=True)

    agg_stats = {
        "markdown": 0,
        "rst": 0,
        "text_other": 0,
        "code_config": 0,
        "svg": 0,
        "media_other": 0,
        "total_files": 0,
        "total_bytes": 0,
    }
    source_records: list[dict[str, Any]] = []

    for idx, src_cfg in enumerate(project["sources"]):
        repo = src_cfg["repo"]
        branch = src_cfg["branch"]
        clone_dir = tmp_base / f"{slug}-{idx}-{repo.replace('/', '_')}"
        repo_url = f"https://github.com/{repo}.git"

        run_git(
            [
                "clone",
                "--depth", "1",
                "--single-branch",
                "--branch", branch,
                "--filter=blob:none",
                "--sparse",
                repo_url,
                str(clone_dir),
            ]
        )

        commit_sha = run_git(["rev-parse", "HEAD"], cwd=clone_dir).strip()
        commit_date = run_git(["show", "-s", "--format=%cI", "HEAD"], cwd=clone_dir).strip()

        resolved_version = None
        resolved_subpath = None
        if "version_resolver" in src_cfg:
            resolved_version, resolved_subpath = resolve_dynamic_path(
                clone_dir, src_cfg["version_resolver"]
            )

        resolved_paths: list[dict[str, Any]] = []
        for p in src_cfg["paths"]:
            raw_src = p["src"]
            if "{resolved_path}" in raw_src:
                assert resolved_subpath is not None
                raw_src = raw_src.replace("{resolved_path}", resolved_subpath)
            resolved_paths.append({
                "src": raw_src,
                "dest": p.get("dest", ""),
                "svg_only": p.get("svg_only", False),
            })

        exclude_dirs = set(src_cfg.get("exclude_dirs", []))
        exclude_files = set(src_cfg.get("exclude_files", []))

        sparse_patterns = build_sparse_patterns(resolved_paths, exclude_dirs, scope)
        # Pass patterns via stdin to avoid argv limits
        proc = subprocess.run(
            ["git", "sparse-checkout", "set", "--no-cone", "--stdin"],
            cwd=str(clone_dir),
            input="\n".join(sparse_patterns) + "\n",
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"sparse-checkout failed for {repo}: {proc.stderr.strip()}"
            )

        src_stats_total = 0
        src_bytes_total = 0
        copied_mappings: list[dict[str, str]] = []

        for p in resolved_paths:
            sub_src = clone_dir / p["src"] if p["src"] else clone_dir
            sub_dest = project_dest / p["dest"] if p["dest"] else project_dest
            exts = allowed_extensions(scope, svg_only=p["svg_only"])
            st = copy_filtered_tree(
                sub_src, sub_dest, exts, exclude_dirs, exclude_files, clone_dir
            )
            for k in agg_stats:
                agg_stats[k] += st[k]
            src_stats_total += st["total_files"]
            src_bytes_total += st["total_bytes"]
            if st["total_files"] > 0 or not p["svg_only"]:
                copied_mappings.append({
                    "upstream_path": p["src"] or "/",
                    "local_subdir": p["dest"] or ".",
                    "svg_only": p["svg_only"],
                })

        license_dest = src_cfg.get("license_dest", "UPSTREAM_LICENSE")
        saved_license = copy_upstream_license(clone_dir, project_dest, license_dest)

        # Clean up temporary clone right away to keep disk usage tiny
        shutil.rmtree(clone_dir, ignore_errors=True)

        source_records.append({
            "repo": repo,
            "url": f"https://github.com/{repo}",
            "branch": branch,
            "commit_sha": commit_sha,
            "commit_date": commit_date,
            "resolved_version": resolved_version,
            "license_file": saved_license,
            "mappings": copied_mappings,
            "files": src_stats_total,
            "bytes": src_bytes_total,
        })

    return {
        "slug": slug,
        "name": project["name"],
        "layer": project["layer"],
        "layer_slug": layer_slug,
        "format": project["format"],
        "website": project["website"],
        "local_path": f"docs/{layer_slug}/{slug}",
        "sources": source_records,
        "stats": agg_stats,
    }


def format_mb(num_bytes: int) -> str:
    return f"{num_bytes / 1_000_000:.2f} MB"


def generate_readme(lock_data: dict[str, Any]) -> str:
    projects = lock_data["projects"]
    total_files = lock_data["totals"]["total_files"]
    total_bytes = lock_data["totals"]["total_bytes"]
    total_md = lock_data["totals"]["markdown"]
    total_rst = lock_data["totals"]["rst"]
    total_code = lock_data["totals"]["code_config"]
    total_svg = lock_data["totals"]["svg"]
    synced_at = lock_data["synced_at_utc"]
    scope = lock_data["scope"]

    lines = [
        "# CNCF Graduated Projects Documentation Backup",
        "",
        "Consolidated, version-pinned documentation corpus covering **all 26 CNCF Graduated projects** across 7 architectural layers, structured for learning, offline reference, and Retrieval-Augmented Generation (RAG).",
        "",
        "## Corpus Summary",
        "",
        f"- **Last synced (UTC):** `{synced_at}`",
        f"- **Backup scope:** `{scope}` (prose docs + config/code examples + vector `.svg` architecture diagrams; latest stable version per project)",
        f"- **Total projects:** `{len(projects)}` (synced from `{sum(len(p['sources']) for p in projects)}` upstream GitHub repositories)",
        f"- **Total files:** `{total_files:,}` (`{total_md:,}` Markdown/MDX, `{total_rst:,}` reStructuredText, `{total_code:,}` YAML/JSON/code examples, `{total_svg:,}` SVG diagrams)",
        f"- **Uncompressed corpus size:** `{format_mb(total_bytes)}`",
        "",
        "## Directory Layout",
        "",
        "```text",
        "cncf-backup/",
        "├── docs/",
        "│   ├── orchestration-core/   # Kubernetes, etcd, containerd, CoreDNS, KubeVirt, Karmada",
        "│   ├── networking-mesh/      # Cilium, Envoy, Istio, Linkerd",
        "│   ├── observability/        # Prometheus (+ Alertmanager), OpenTelemetry, Jaeger, Fluentd",
        "│   ├── gitops-packaging/     # Helm, Argo (CD, Workflows, Rollouts), Flux",
        "│   ├── security-identity/    # SPIFFE/SPIRE, OPA, Kyverno, cert-manager, Falco, Harbor",
        "│   ├── storage-messaging/    # Rook, NATS",
        "│   └── ai-ml/                # Kubeflow",
        "├── manifest/",
        "│   ├── projects.json         # Declarative source definitions & dynamic version resolvers",
        "│   └── lock.json             # Exact upstream commit SHAs, timestamps, mappings & file counts",
        "└── scripts/",
        "    ├── sync_docs.py          # Repeatable parallel sparse-checkout sync tool (Python 3 stdlib)",
        "    └── export_jsonl.py       # Export prose/code docs + pinned GitHub URLs to JSONL for RAG",
        "```",
        "",
        "## Project Inventory",
        "",
        "| Layer | Project | Local Path | Upstream Repo & Path | Pin (`SHA`) | Format | Files | Size |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | ---: | ---: |",
    ]

    for p in projects:
        src_parts = []
        sha_parts = []
        for s in p["sources"]:
            repo = s["repo"]
            short_sha = s["commit_sha"][:7]
            non_svg_paths = [m["upstream_path"] for m in s["mappings"] if not m.get("svg_only")]
            path_label = ", ".join(non_svg_paths) if non_svg_paths else "/"
            src_parts.append(f"[`{repo}`](https://github.com/{repo}) (`{path_label}`)")
            sha_parts.append(f"[`{short_sha}`](https://github.com/{repo}/tree/{s['commit_sha']})")

        fmt_label = "reStructuredText (`.rst`)" if p["format"] == "rst" else "Markdown"
        local_link = f"[`{p['local_path']}/`]({p['local_path']})"
        lines.append(
            f"| {p['layer']} | **{p['name']}** | {local_link} | "
            f"{'<br>'.join(src_parts)} | {'<br>'.join(sha_parts)} | "
            f"{fmt_label} | {p['stats']['total_files']:,} | {format_mb(p['stats']['total_bytes'])} |"
        )

    lines.extend([
        "",
        "## Keeping the Backup Updated",
        "",
        "`scripts/sync_docs.py` uses `git clone --depth 1 --filter=blob:none --sparse` with no third-party Python dependencies:",
        "",
        "```bash",
        "# Re-sync all 26 CNCF Graduated projects (default scope: text-svg)",
        "python3 scripts/sync_docs.py",
        "",
        "# Re-sync specific project(s) only",
        "python3 scripts/sync_docs.py --project kubernetes --project cilium",
        "",
        "# Switch backup scope if desired (text-only | text-svg | all-media)",
        "python3 scripts/sync_docs.py --scope text-only",
        "```",
        "",
        "## Using This Corpus for Retrieval / RAG",
        "",
        "```bash",
        "# Export all prose docs (.md/.mdx/.rst/.txt) with extracted titles & pinned GitHub blob URLs",
        "python3 scripts/export_jsonl.py --output corpus.jsonl",
        "",
        "# Include standalone YAML/JSON/code example files as well",
        "python3 scripts/export_jsonl.py --include-code --output corpus_with_code.jsonl",
        "```",
        "",
        "1. **Provenance & deep-linking (`manifest/lock.json`):** Every project entry in `manifest/lock.json` records its exact `commit_sha`, `upstream_path`, and `local_subdir`, allowing your ingestion pipeline to attach canonical GitHub source URLs and CNCF layer metadata to each chunk.",
        "2. **File formats:**",
        "   - **Markdown / MDX (`.md`, `.mdx`):** 24 of 26 projects. Note that Hugo/Docusaurus/Starlight frontmatter (`--- ... ---`) at the top of files contains clean `title`, `description`, and `weight` metadata useful for hybrid search.",
        "   - **reStructuredText (`.rst`):** Cilium and Envoy use Sphinx `.rst` directives (`.. code-block::`, `.. note::`, `:ref:`).",
        "3. **Licenses:** Upstream `UPSTREAM_LICENSE*` files are preserved inside each project directory alongside the documentation.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync CNCF Graduated Project docs.")
    parser.add_argument(
        "--scope",
        choices=["text-only", "text-svg", "all-media"],
        default=None,
        help="File filter scope (default: from manifest/projects.json -> text-svg)",
    )
    parser.add_argument(
        "--project",
        action="append",
        dest="projects",
        help="Sync only specific project slug(s); may be passed multiple times.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Number of concurrent project sync workers (default: 6).",
    )
    args = parser.parse_args()

    manifest = json.loads(PROJECTS_MANIFEST.read_text(encoding="utf-8"))
    scope = args.scope or manifest.get("default_scope", "text-svg")
    all_projects: list[dict[str, Any]] = manifest["projects"]

    if args.projects:
        wanted = set(args.projects)
        known = {p["slug"] for p in all_projects}
        unknown = wanted - known
        if unknown:
            print(f"Error: unknown project slug(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
        target_projects = [p for p in all_projects if p["slug"] in wanted]
    else:
        target_projects = all_projects

    print(f"Syncing {len(target_projects)} project(s) with scope='{scope}' (workers={args.workers})...")
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    results_by_slug: dict[str, dict[str, Any]] = {}
    with tempfile.TemporaryDirectory(prefix="cncf-sync-") as tmp_str:
        tmp_base = Path(tmp_str)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            future_map = {
                pool.submit(sync_project, proj, scope, tmp_base): proj["slug"]
                for proj in target_projects
            }
            for fut in concurrent.futures.as_completed(future_map):
                slug = future_map[fut]
                res = fut.result()
                results_by_slug[slug] = res
                st = res["stats"]
                print(
                    f"  [OK] {res['name']:32s} -> {res['local_path']:38s} "
                    f"({st['total_files']:4d} files, {format_mb(st['total_bytes'])})",
                    flush=True,
                )

    # Merge with existing lock.json if partial sync
    existing_by_slug: dict[str, dict[str, Any]] = {}
    if args.projects and LOCK_MANIFEST.is_file():
        old_lock = json.loads(LOCK_MANIFEST.read_text(encoding="utf-8"))
        for p in old_lock.get("projects", []):
            existing_by_slug[p["slug"]] = p
    existing_by_slug.update(results_by_slug)

    ordered_records = [
        existing_by_slug[p["slug"]]
        for p in all_projects
        if p["slug"] in existing_by_slug
    ]

    totals = {
        "markdown": 0,
        "rst": 0,
        "text_other": 0,
        "code_config": 0,
        "svg": 0,
        "media_other": 0,
        "total_files": 0,
        "total_bytes": 0,
    }
    for rec in ordered_records:
        for k in totals:
            totals[k] += rec["stats"][k]

    lock_data = {
        "schema_version": 1,
        "synced_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": scope,
        "project_count": len(ordered_records),
        "totals": totals,
        "projects": ordered_records,
    }

    LOCK_MANIFEST.write_text(json.dumps(lock_data, indent=2) + "\n", encoding="utf-8")
    README_PATH.write_text(generate_readme(lock_data), encoding="utf-8")

    print("-" * 80)
    print(
        f"Completed! {len(ordered_records)} projects | "
        f"{totals['total_files']:,} files | {format_mb(totals['total_bytes'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
