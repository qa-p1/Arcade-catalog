#!/usr/bin/env python3
"""Build shortcuts/index.json from the shortcut sheets in shortcuts/."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_NAME = "index.json"


class IndexBuildError(ValueError):
    """A shortcut sheet cannot be represented in the generated index."""


def build_index(root: Path = ROOT) -> dict[str, Any]:
    """Return the generated index object without writing it."""
    root = Path(root)
    sheets_dir = root / "shortcuts"
    entries: list[dict[str, Any]] = []
    if not sheets_dir.exists():
        return {"schema": 1, "sheets": entries}

    for path in sorted(sheets_dir.glob("*.json")):
        if path.name == INDEX_NAME:
            continue
        relative = path.relative_to(root).as_posix()
        try:
            sheet = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise IndexBuildError(f"{relative}: cannot read JSON: {exc}") from exc
        if not isinstance(sheet, dict):
            raise IndexBuildError(f"{relative}: sheet must be a JSON object")
        for key, expected in (("id", str), ("name", str), ("match", dict)):
            if not isinstance(sheet.get(key), expected):
                raise IndexBuildError(f"{relative}: field {key!r} is required and must be {expected.__name__}")
        entries.append(
            {
                "id": sheet["id"],
                "name": sheet["name"],
                "file": relative,
                "match": sheet["match"],
            }
        )

    entries.sort(key=lambda entry: entry["id"])
    return {"schema": 1, "sheets": entries}


def write_index(root: Path = ROOT) -> Path:
    """Write the generated index and return its path."""
    root = Path(root)
    path = root / "shortcuts" / INDEX_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_index(root), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="catalog root (defaults to this repository)")
    parser.add_argument("--check", action="store_true", help="check whether the index is current without writing it")
    args = parser.parse_args()

    try:
        expected = build_index(args.root)
    except IndexBuildError as exc:
        print(f"ERROR: {exc}")
        return 1

    index_path = args.root / "shortcuts" / INDEX_NAME
    if args.check:
        try:
            actual = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            print(f"ERROR: {index_path}: cannot read index JSON: {exc}")
            return 1
        if actual != expected:
            print(f"ERROR: {index_path}: index is out of date; run python3 scripts/build_index.py")
            return 1
        print(f"{index_path.relative_to(args.root)} is up to date")
        return 0

    try:
        write_index(args.root)
    except OSError as exc:
        print(f"ERROR: {index_path}: cannot write index: {exc}")
        return 1
    print(f"Wrote {index_path.relative_to(args.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
