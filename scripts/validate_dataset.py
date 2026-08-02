#!/usr/bin/env python3
"""Validate data/test_cases.jsonl against schema/test_case.schema.json.

Pure-stdlib check (required fields, enum values, no unexpected fields,
no duplicate ids) so contributors don't need to install anything to
validate a PR before opening it.

Usage:
    python scripts/validate_dataset.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "test_case.schema.json"
DATA_PATH = ROOT / "data" / "test_cases.jsonl"


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate_case(case: dict, schema: dict, line_no: int) -> list:
    errors = []
    for field in schema["required"]:
        if field not in case:
            errors.append(f"line {line_no} ({case.get('id', '?')}): missing required field '{field}'")
    for field, spec in schema["properties"].items():
        if field in case and "enum" in spec and case[field] not in spec["enum"]:
            errors.append(f"line {line_no} ({case.get('id', '?')}): '{field}' = {case[field]!r} not in {spec['enum']}")
    allowed = set(schema["properties"])
    extra = set(case) - allowed
    if extra and schema.get("additionalProperties") is False:
        errors.append(f"line {line_no} ({case.get('id', '?')}): unexpected fields {sorted(extra)}")
    return errors


def main():
    schema = load_schema()
    seen_ids = set()
    all_errors = []

    with open(DATA_PATH, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"line {line_no}: invalid JSON ({e})")
                continue
            all_errors.extend(validate_case(case, schema, line_no))
            cid = case.get("id")
            if cid in seen_ids:
                all_errors.append(f"line {line_no}: duplicate id '{cid}'")
            seen_ids.add(cid)

    if all_errors:
        print(f"FAILED - {len(all_errors)} issue(s):")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"OK - {len(seen_ids)} test cases valid.")


if __name__ == "__main__":
    main()
