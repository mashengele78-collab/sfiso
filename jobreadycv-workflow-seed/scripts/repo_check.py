#!/usr/bin/env python3
"""Dependency-free repository hygiene checks for the JobReadyCV workflow repo."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

DISALLOWED_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".odt",
    ".rtf",
    ".pages",
    ".zip",
    ".7z",
    ".rar",
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".tif",
    ".tiff",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}
DISALLOWED_PARTS = {
    "clients",
    "client-data",
    "orders",
    "working",
    "exports",
    "deliveries",
    "uploads",
    "whatsapp",
    "secrets",
}
SKIP_PARTS = {".git", "__pycache__", "node_modules"}
MAX_FILE_BYTES = 1_000_000
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ORDER_ID = re.compile(r"^JRCV-[0-9]{8}-[A-Z0-9]{6}$")


def files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_PARTS)
    )


def check_paths(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(ROOT)
        parts = set(relative.parts[:-1])
        if parts & DISALLOWED_PARTS:
            errors.append(f"prohibited data directory: {relative}")
        if path.suffix.lower() in DISALLOWED_SUFFIXES:
            errors.append(f"prohibited customer/binary file type: {relative}")
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            errors.append(f"prohibited environment file: {relative}")
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"file exceeds {MAX_FILE_BYTES} bytes: {relative}")
        if b"\x00" in path.read_bytes()[:8192]:
            errors.append(f"binary file is not allowed: {relative}")


def check_json(paths: list[Path], errors: list[str]) -> None:
    parsed: dict[Path, object] = {}
    for path in paths:
        if path.suffix == ".json":
            try:
                parsed[path] = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")

    example_path = ROOT / "examples" / "order-manifest.example.json"
    example = parsed.get(example_path)
    if not isinstance(example, dict):
        errors.append("synthetic order-manifest example is missing or not an object")
        return

    expected_keys = {
        "schema_version",
        "order_id",
        "created_on",
        "jurisdiction",
        "services",
        "status",
        "consent_recorded",
        "source_facts_checked",
        "human_review_approved",
        "output_formats",
    }
    if set(example) != expected_keys:
        errors.append("synthetic order-manifest example has unexpected or missing fields")
    order_id = example.get("order_id")
    if not isinstance(order_id, str) or not ORDER_ID.fullmatch(order_id):
        errors.append("synthetic order-manifest example has an invalid order_id")
    if not isinstance(order_id, str) or not order_id.startswith("JRCV-2099"):
        errors.append("example order_id must remain obviously synthetic (year 2099)")
    if example.get("created_on") != "2099-01-01":
        errors.append("example created_on must remain obviously synthetic")


def check_markdown_links(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if path.suffix.lower() not in {".md", ".markdown"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"Markdown is not UTF-8: {path.relative_to(ROOT)}: {exc}")
            continue
        for target in MARKDOWN_LINK.findall(text):
            clean_target = target.strip().split(maxsplit=1)[0].strip("<>\"")
            if not clean_target or clean_target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            clean_target = unquote(clean_target.split("#", 1)[0])
            destination = (path.parent / clean_target).resolve()
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"relative link escapes repository in {path.relative_to(ROOT)}: {target}")
                continue
            if not destination.exists():
                errors.append(f"broken relative link in {path.relative_to(ROOT)}: {target}")


def main() -> int:
    errors: list[str] = []
    repository_files = files()
    check_paths(repository_files, errors)
    check_json(repository_files, errors)
    check_markdown_links(repository_files, errors)

    if errors:
        print("Repository check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Repository check passed: {len(repository_files)} files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
