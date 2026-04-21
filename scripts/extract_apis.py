#!/usr/bin/env python3
"""
extract_apis.py - Extract REST API endpoints from BTSE Slate documentation.

Modes:
  Full scan   (default, or when llms.txt does not exist):
              Scans all latest-version source files and writes llms.txt from scratch.

  Incremental (when --base-ref is provided):
              Uses `git diff` to find only the changed source files.
              Updates only those sections in llms.txt; everything else is untouched.
              Appends a delta entry to ## Recent Changes inside llms.txt.
              No separate delta file is created.

Usage:
    python scripts/extract_apis.py                          # full scan (initial)
    python scripts/extract_apis.py --base-ref origin/main  # incremental (PR)
    python scripts/extract_apis.py --base-ref HEAD~1        # incremental (push)
"""

import re
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Product configuration
# ---------------------------------------------------------------------------

# Only the latest version of each product.
# earn excluded: its endpoints (/api/v3.2/invest/…) are already covered at
# v3.3 by spotV3_3.
LATEST_PRODUCTS = {
    "spotV3_3",     # supersedes spot (v3.2)
    "futuresV2_3",  # supersedes futuresV2_2 and futures
    "wallet",
    "otc",
    "streaming",
    "fix",
}

PRODUCT_ORDER = ["spotV3_3", "futuresV2_3", "wallet", "otc", "streaming", "fix"]

PRODUCT_LABELS = {
    "spotV3_3":    "Spot API v3.3",
    "futuresV2_3": "Futures API v2.3",
    "wallet":      "Wallet API",
    "otc":         "OTC API",
    "streaming":   "Streaming / WebSocket API",
    "fix":         "FIX Protocol API",
}

BASE_URLS = {
    "spotV3_3":    "https://api.btse.com/spot",
    "futuresV2_3": "https://api.btse.com/futures",
    "wallet":      "https://api.btse.com/spot",
    "otc":         "https://api.btse.com/otc",
    "streaming":   "wss://ws.btse.com/ws/otc",
    "fix":         "tcp+ssl://fix.btse.com:9876",
}

# ---------------------------------------------------------------------------
# Regex constants
# ---------------------------------------------------------------------------

URL_RE          = re.compile(r"`(GET|POST|PUT|DELETE|PATCH)\s+(/api/[^\s`]+)`")
VERSION_RE      = re.compile(r"^/api/v(\d+)\.(\d+)/")
ENDPOINT_LINE_RE = re.compile(r"^`(GET|POST|PUT|DELETE|PATCH)")
SECTION_H2_RE   = re.compile(r"^## ([^#].+)$")
SECTION_H3_RE   = re.compile(r"^### (.+)$")
PERMISSION_RE   = re.compile(r"`?(Trading|Read|Wallet|Transfer|Order)`?\s+permission", re.IGNORECASE)
SOURCE_LINE_RE  = re.compile(r"^# source: (.+)$")
METHOD_LINE_RE  = re.compile(r"^(GET|POST|PUT|DELETE|PATCH) (/api/\S+)$")
GENERATED_RE    = re.compile(r"^<!-- generated: .+ \| total: \d+ endpoints -->$", re.MULTILINE)

_CHANGES_MARKER = "\n---\n\n## Recent Changes"


# ---------------------------------------------------------------------------
# Version helpers (deduplicate dual-version lines like /api/v3.2/foo or /api/v3.3/foo)
# ---------------------------------------------------------------------------

def _path_version(path: str) -> tuple[int, int]:
    m = VERSION_RE.match(path)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def _canonical_path(path: str) -> str:
    return VERSION_RE.sub("/", path)


def _dedup_by_version(matches: list[tuple[str, str]]) -> list[tuple[str, str]]:
    best: dict[tuple[str, str], tuple[str, str]] = {}
    for method, path in matches:
        key = (method, _canonical_path(path))
        if key not in best or _path_version(path) > _path_version(best[key][1]):
            best[key] = (method, path)
    return list(best.values())


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Endpoint:
    method: str
    path: str
    section: str
    description: str
    source: str
    auth: str
    permission: str
    required_params: list[str] = field(default_factory=list)

    def key(self) -> str:
        return f"{self.method} {self.path}"

    def full_url(self, product: str) -> str:
        base = BASE_URLS.get(product, "")
        return f"{base}{self.path}" if base else self.path

    def sig(self) -> str:
        """Fingerprint used to detect modifications."""
        params = ", ".join(self.required_params) if self.required_params else "none"
        auth_str = self.auth + (f"  Permission: {self.permission}" if self.permission else "")
        return f"{self.description}|{auth_str}|{params}"


# ---------------------------------------------------------------------------
# Request parameter parsing
# ---------------------------------------------------------------------------

def extract_required_params(lines: list[str], start: int) -> list[str]:
    in_section = False
    header_parsed = False
    required_col = -1
    params: list[str] = []

    i = start
    while i < len(lines):
        line = lines[i]
        if SECTION_H2_RE.match(line):
            break
        if re.match(r"^### Request Parameters", line, re.IGNORECASE):
            in_section, header_parsed, required_col = True, False, -1
            i += 1
            continue
        if in_section and SECTION_H3_RE.match(line):
            break
        if in_section and "|" in line:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not cells:
                i += 1
                continue
            if not header_parsed:
                for idx, cell in enumerate(cells):
                    if cell.lower() == "required":
                        required_col = idx
                header_parsed = True
                i += 1
                continue
            if all(re.match(r"^[-: ]+$", c) for c in cells if c):
                i += 1
                continue
            if required_col >= 0 and len(cells) > required_col:
                if cells[required_col].lower() in ("yes", "y", "true"):
                    name = cells[0].strip("`* ")
                    if name:
                        params.append(name)
        i += 1
    return params


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def _extract_permission(prose: str) -> tuple[str, str]:
    m = PERMISSION_RE.search(prose)
    return ("HMAC-SHA384", m.group(1).capitalize()) if m else ("None (public)", "")


def parse_markdown_content(content: str, rel_source: str) -> list[Endpoint]:
    """Parse markdown text and return all API endpoints found."""
    lines = content.split("\n")
    endpoints: list[Endpoint] = []
    current_section = ""

    for i, line in enumerate(lines):
        m = SECTION_H2_RE.match(line)
        if m:
            current_section = m.group(1).strip()
            continue

        if not ENDPOINT_LINE_RE.match(line):
            continue
        if re.search(r"\(deprecated\)", current_section, re.IGNORECASE):
            continue

        matches = _dedup_by_version(URL_RE.findall(line))
        if not matches:
            continue

        prose_lines: list[str] = []
        desc_end = i
        for j in range(i + 1, min(i + 12, len(lines))):
            c = lines[j].strip()
            if not c:
                continue
            if c.startswith(("#", "|", ">", "```")) or URL_RE.search(c):
                break
            prose_lines.append(c)
            desc_end = j

        description = prose_lines[0] if prose_lines else ""
        auth, permission = _extract_permission(" ".join(prose_lines))
        required_params = extract_required_params(lines, desc_end + 1)

        for method, path in matches:
            endpoints.append(Endpoint(
                method=method, path=path, section=current_section,
                description=description, source=rel_source,
                auth=auth, permission=permission, required_params=required_params,
            ))
    return endpoints


def parse_markdown(filepath: Path, source_dir: Path) -> list[Endpoint]:
    return parse_markdown_content(
        filepath.read_text(encoding="utf-8"),
        str(filepath.relative_to(source_dir)),
    )


def collect_all_endpoints(source_dir: Path) -> dict[str, list[Endpoint]]:
    result: dict[str, list[Endpoint]] = {}
    for md_file in sorted(source_dir.glob("*/en/index.html.md")):
        product = md_file.parts[-3]
        if product not in LATEST_PRODUCTS:
            continue
        eps = parse_markdown(md_file, source_dir)
        if eps:
            result[str(md_file.relative_to(source_dir))] = eps
    return result


# ---------------------------------------------------------------------------
# llms.txt section formatting
# ---------------------------------------------------------------------------

_STATIC_HEADER = """\
# BTSE REST API

> BTSE is a cryptocurrency exchange. This file lists all REST API endpoints \
for use by LLM agents, AI code-generation tools, and automated integrations.

## Authentication

All private endpoints require HMAC-SHA384 request signing. Include these \
three headers in every authenticated request:

- `request-api`: your API key (string)
- `request-nonce`: current timestamp in milliseconds (integer as string)
- `request-sign`: HMAC-SHA384(secret, urlpath + nonce + body)

Public (market-data) endpoints require no authentication.

---"""


def format_product_section(source_key: str, eps: list[Endpoint]) -> str:
    product = Path(source_key).parts[0]
    label   = PRODUCT_LABELS.get(product, product)
    base_url = BASE_URLS.get(product, "")

    lines = [f"## {label}", f"# source: {source_key}", ""]
    if base_url:
        lines += [f"Base URL: {base_url}", ""]

    sections: dict[str, list[Endpoint]] = {}
    for ep in eps:
        sections.setdefault(ep.section, []).append(ep)

    for section, section_eps in sections.items():
        if section:
            lines += [f"### {section}", ""]
        for ep in section_eps:
            auth_str = ep.auth + (f"  Permission: {ep.permission}" if ep.permission else "")
            params_str = ", ".join(ep.required_params) if ep.required_params else "none"
            lines += [
                ep.key(),
                f"Full URL: {ep.full_url(product)}",
                f"Auth: {auth_str}",
                *([ f"Description: {ep.description}"] if ep.description else []),
                f"Required params: {params_str}",
                "",
            ]
    return "\n".join(lines)


def build_llms_full(eps_by_source: dict[str, list[Endpoint]], generated_at: str) -> str:
    total = sum(len(v) for v in eps_by_source.values())
    parts = [_STATIC_HEADER, "",
             f"<!-- generated: {generated_at} | total: {total} endpoints -->", ""]

    ordered: list[str] = []
    for product in PRODUCT_ORDER:
        for src in sorted(eps_by_source):
            if Path(src).parts[0] == product and src not in ordered:
                ordered.append(src)
    for src in sorted(eps_by_source):
        if src not in ordered:
            ordered.append(src)

    for src in ordered:
        parts += [format_product_section(src, eps_by_source[src]), ""]

    return "\n".join(parts).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# llms.txt parsing (for incremental updates)
# ---------------------------------------------------------------------------

def parse_llms_file(content: str) -> tuple[str, dict[str, str], list[str], str]:
    """
    Split llms.txt into:
      header        – static preamble (title, auth section, ---, meta comment)
      sections      – {source_key: section_text}
      section_order – source keys in file order
      changes       – ## Recent Changes block text (may be "")
    """
    # Peel off the Recent Changes footer first
    changes = ""
    idx = content.find(_CHANGES_MARKER)
    if idx >= 0:
        changes = content[idx + 1:]  # keep the "---\n\n## Recent Changes…" text
        content = content[:idx]

    lines = content.split("\n")

    # Find (line_index, source_key) for every product section
    section_starts: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = SOURCE_LINE_RE.match(line)
        if m:
            # The ## heading is the non-empty line just above
            for j in range(i - 1, max(i - 4, -1), -1):
                if SECTION_H2_RE.match(lines[j]):
                    section_starts.append((j, m.group(1)))
                    break

    if not section_starts:
        return content, {}, [], changes

    header = "\n".join(lines[: section_starts[0][0]]).rstrip()
    sections: dict[str, str] = {}
    section_order: list[str] = []

    for idx2, (start, key) in enumerate(section_starts):
        end = section_starts[idx2 + 1][0] if idx2 + 1 < len(section_starts) else len(lines)
        sections[key] = "\n".join(lines[start:end]).rstrip()
        section_order.append(key)

    return header, sections, section_order, changes


def _count_endpoints(sections: dict[str, str]) -> int:
    return sum(
        sum(1 for line in s.split("\n") if METHOD_LINE_RE.match(line))
        for s in sections.values()
    )


def rebuild_llms(
    header: str,
    sections: dict[str, str],
    section_order: list[str],
    changes: str,
    generated_at: str,
) -> str:
    total = _count_endpoints(sections)
    meta  = f"<!-- generated: {generated_at} | total: {total} endpoints -->"
    header = GENERATED_RE.sub(meta, header) if GENERATED_RE.search(header) \
             else header.rstrip() + "\n\n" + meta

    parts = [header.rstrip(), ""]
    for key in section_order:
        if key in sections:
            # Two empty strings = two blank lines between sections,
            # matching the spacing produced by build_llms_full.
            parts += [sections[key].rstrip(), "", ""]

    if changes:
        parts.append(changes.rstrip())

    return "\n".join(parts).rstrip("\n") + "\n"


def parse_section_endpoints(section_text: str) -> dict[str, Endpoint]:
    """Parse a product section from llms.txt into {key: Endpoint}."""
    result: dict[str, Endpoint] = {}
    source = ""
    lines = section_text.split("\n")

    for line in lines:
        m = SOURCE_LINE_RE.match(line)
        if m:
            source = m.group(1)
            break

    i = 0
    while i < len(lines):
        m = METHOD_LINE_RE.match(lines[i])
        if m:
            ep = Endpoint(method=m.group(1), path=m.group(2), section="",
                          description="", source=source, auth="", permission="")
            for j in range(i + 1, min(i + 8, len(lines))):
                ln = lines[j]
                if ln.startswith("Auth: "):
                    parts = ln[6:].split("  Permission: ")
                    ep.auth = parts[0]
                    ep.permission = parts[1] if len(parts) > 1 else ""
                elif ln.startswith("Description: "):
                    ep.description = ln[13:]
                elif ln.startswith("Required params: "):
                    val = ln[17:]
                    ep.required_params = [] if val == "none" else val.split(", ")
                elif ln == "" or METHOD_LINE_RE.match(ln):
                    break
            result[ep.key()] = ep
        i += 1
    return result


# ---------------------------------------------------------------------------
# Git utilities
# ---------------------------------------------------------------------------

def _git(*args: str) -> str:
    return subprocess.check_output(["git"] + list(args), text=True)


def get_changed_source_files(base_ref: str, source_dir: Path) -> list[Path]:
    """Return source markdown files that changed between base_ref and HEAD."""
    try:
        output = _git("diff", "--name-only", base_ref, "HEAD")
    except subprocess.CalledProcessError:
        print(f"Warning: git diff failed for ref '{base_ref}'", file=sys.stderr)
        return []

    changed: list[Path] = []
    for rel in output.strip().split("\n"):
        if not rel:
            continue
        p = Path(rel)
        if (len(p.parts) == 4
                and p.parts[0] == source_dir.name
                and p.parts[1] in LATEST_PRODUCTS
                and p.parts[2] == "en"
                and p.parts[3] == "index.html.md"):
            full = Path.cwd() / p
            if full.exists():
                changed.append(full)
    return changed


def get_old_content(filepath: Path, base_ref: str) -> Optional[str]:
    """Return file content at base_ref, or None if the file is new."""
    try:
        repo_root = _git("rev-parse", "--show-toplevel").strip()
        rel = filepath.relative_to(repo_root)
        return _git("show", f"{base_ref}:{rel}")
    except (subprocess.CalledProcessError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Delta computation and formatting
# ---------------------------------------------------------------------------

@dataclass
class Delta:
    added:    list[Endpoint]                    = field(default_factory=list)
    removed:  list[Endpoint]                    = field(default_factory=list)
    modified: list[tuple[Endpoint, Endpoint]]   = field(default_factory=list)

    def is_empty(self) -> bool:
        return not self.added and not self.removed and not self.modified


def compute_delta(old: dict[str, Endpoint], new: dict[str, Endpoint]) -> Delta:
    d = Delta()
    for key, ep in new.items():
        if key not in old:
            d.added.append(ep)
        elif old[key].sig() != ep.sig():
            d.modified.append((old[key], ep))
    for key, ep in old.items():
        if key not in new:
            d.removed.append(ep)
    return d


def format_delta_entry(delta: Delta, generated_at: str) -> str:
    if delta.is_empty():
        return ""

    lines = [f"### {generated_at}"]

    if delta.added:
        lines.append(f"**Added ({len(delta.added)}):**")
        for ep in sorted(delta.added, key=lambda e: e.key()):
            auth = ep.auth + (f"  Permission: {ep.permission}" if ep.permission else "")
            desc = f" — {ep.description}" if ep.description else ""
            lines.append(f"+ {ep.key()}{desc}  [{auth}]")

    if delta.removed:
        lines.append(f"**Removed ({len(delta.removed)}):**")
        for ep in sorted(delta.removed, key=lambda e: e.key()):
            desc = f" — {ep.description}" if ep.description else ""
            lines.append(f"- {ep.key()}{desc}")

    if delta.modified:
        lines.append(f"**Modified ({len(delta.modified)}):**")
        for old, new in sorted(delta.modified, key=lambda t: t[0].key()):
            lines.append(f"~ {old.key()}")
            for attr in ("description", "auth", "required_params"):
                ov = ", ".join(getattr(old, attr)) if attr == "required_params" else getattr(old, attr)
                nv = ", ".join(getattr(new, attr)) if attr == "required_params" else getattr(new, attr)
                if ov != nv:
                    lines.append(f"  {attr}: {ov!r} → {nv!r}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Full scan mode
# ---------------------------------------------------------------------------

def run_full(source_dir: Path, output_path: Path) -> None:
    print(f"Full scan of {source_dir} ...")
    eps_by_source = collect_all_endpoints(source_dir)

    if not eps_by_source:
        print("No endpoints found.", file=sys.stderr)
        sys.exit(1)

    for src, eps in sorted(eps_by_source.items()):
        print(f"  {src}: {len(eps)} endpoints")

    total = sum(len(v) for v in eps_by_source.values())
    print(f"Total: {total} endpoints")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    output_path.write_text(build_llms_full(eps_by_source, generated_at), encoding="utf-8")
    print(f"Written: {output_path}  ({output_path.stat().st_size} bytes)")


# ---------------------------------------------------------------------------
# Incremental mode
# ---------------------------------------------------------------------------

def run_incremental(source_dir: Path, output_path: Path, base_ref: str) -> str:
    """
    Update llms.txt using git diff against base_ref.
    Returns the latest delta entry text (used for the PR comment).
    """
    if not output_path.exists():
        print("llms.txt not found — falling back to full scan")
        run_full(source_dir, output_path)
        return "Initial generation — full scan performed."

    changed_files = get_changed_source_files(base_ref, source_dir)
    if not changed_files:
        print("No relevant source files changed — llms.txt unchanged")
        return "No changes detected."

    print(f"Changed files ({len(changed_files)}):")
    for f in changed_files:
        print(f"  {f}")

    existing = output_path.read_text(encoding="utf-8")
    header, sections, section_order, changes_block = parse_llms_file(existing)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    all_delta = Delta()

    for filepath in changed_files:
        rel_key = str(filepath.relative_to(source_dir))

        # Old endpoints: prefer git content, fallback to existing llms.txt section
        old_content = get_old_content(filepath, base_ref)
        if old_content is not None:
            old_eps = {ep.key(): ep for ep in parse_markdown_content(old_content, rel_key)}
        elif rel_key in sections:
            old_eps = parse_section_endpoints(sections[rel_key])
        else:
            old_eps = {}

        # New endpoints: parse current file
        new_ep_list = parse_markdown(filepath, source_dir)
        new_eps = {ep.key(): ep for ep in new_ep_list}

        delta = compute_delta(old_eps, new_eps)
        all_delta.added.extend(delta.added)
        all_delta.removed.extend(delta.removed)
        all_delta.modified.extend(delta.modified)

        # Update the section
        if new_ep_list:
            sections[rel_key] = format_product_section(rel_key, new_ep_list)
            if rel_key not in section_order:
                product = Path(rel_key).parts[0]
                insert_pos = next(
                    (i + 1 for i, k in enumerate(section_order)
                     if PRODUCT_ORDER.index(Path(k).parts[0]) < PRODUCT_ORDER.index(product)),
                    0,
                )
                section_order.insert(insert_pos, rel_key)
        else:
            sections.pop(rel_key, None)
            if rel_key in section_order:
                section_order.remove(rel_key)

        print(f"  {rel_key}: +{len(delta.added)} -{len(delta.removed)} ~{len(delta.modified)}")

    # Build and prepend delta entry to Recent Changes
    delta_entry = format_delta_entry(all_delta, generated_at)
    if delta_entry:
        inner = changes_block.lstrip()
        if inner.startswith("---\n\n## Recent Changes"):
            inner = inner[len("---\n\n## Recent Changes"):].lstrip("\n")
        new_changes = "---\n\n## Recent Changes\n\n" + delta_entry + inner
    else:
        new_changes = changes_block

    output_path.write_text(
        rebuild_llms(header, sections, section_order, new_changes, generated_at),
        encoding="utf-8",
    )
    print(f"Written: {output_path}  ({output_path.stat().st_size} bytes)")
    return delta_entry or "No changes detected."


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract REST API endpoints from BTSE Slate documentation"
    )
    parser.add_argument("--source-dir", default="source",
                        help="Path to the Slate source directory (default: source)")
    parser.add_argument("--output", default="source/llms.txt",
                        help="Output file (default: source/llms.txt)")
    parser.add_argument(
        "--base-ref",
        help="Git ref to diff against for incremental update "
             "(e.g. origin/main, HEAD~1). Omit to run a full scan.",
    )
    args = parser.parse_args()

    source_dir  = Path(args.source_dir)
    output_path = Path(args.output)

    if not source_dir.is_dir():
        print(f"ERROR: source directory '{source_dir}' not found", file=sys.stderr)
        sys.exit(1)

    if args.base_ref:
        delta = run_incremental(source_dir, output_path, args.base_ref)
        print("\n--- Delta ---")
        print(delta)
    else:
        run_full(source_dir, output_path)


if __name__ == "__main__":
    main()
