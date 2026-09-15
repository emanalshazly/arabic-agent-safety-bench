from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


REQUIRED = {
    "case_id", "language", "dialect", "category", "is_adversarial",
    "trusted_task", "untrusted_content", "tools", "protected_canaries",
    "forbidden_actions", "expected_decision", "provenance", "review_status",
}
LANGUAGES = {"ar", "mixed_ar_en"}
DIALECTS = {"msa", "egyptian", "gulf"}
CATEGORIES = {
    "instruction_override", "data_exfiltration", "malicious_tool_use",
    "multilingual_confusion", "benign_control",
}
DECISIONS = {"complete_task", "ignore_untrusted_instruction", "refuse_untrusted_instruction"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    category_counts: Counter[str] = Counter()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            case = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        missing = REQUIRED - set(case)
        if missing:
            errors.append(f"line {line_number}: missing {sorted(missing)}")
            continue
        case_id = case["case_id"]
        if not re.fullmatch(r"aasb_\d{4}", case_id): errors.append(f"line {line_number}: invalid case_id")
        if case_id in seen: errors.append(f"line {line_number}: duplicate case_id {case_id}")
        seen.add(case_id)
        if case["language"] not in LANGUAGES: errors.append(f"line {line_number}: invalid language")
        if case["dialect"] not in DIALECTS: errors.append(f"line {line_number}: invalid dialect")
        if case["category"] not in CATEGORIES: errors.append(f"line {line_number}: invalid category")
        if case["expected_decision"] not in DECISIONS: errors.append(f"line {line_number}: invalid expected_decision")
        if case["provenance"] != "original_synthetic": errors.append(f"line {line_number}: unsupported provenance")
        if case["review_status"] not in {"draft", "native_reviewed"}: errors.append(f"line {line_number}: invalid review_status")
        if not all(isinstance(case[field], list) for field in ("tools", "protected_canaries", "forbidden_actions")):
            errors.append(f"line {line_number}: tools/canaries/actions must be arrays")
        else:
            if not set(case["forbidden_actions"]).issubset(set(case["tools"])):
                errors.append(f"line {line_number}: forbidden_actions must be available tools")
            for field in ("tools", "protected_canaries", "forbidden_actions"):
                if len(case[field]) != len(set(case[field])):
                    errors.append(f"line {line_number}: duplicate value in {field}")
        is_benign = case["category"] == "benign_control"
        if is_benign == bool(case["is_adversarial"]):
            errors.append(f"line {line_number}: category/adversarial flag mismatch")
        if case["category"] == "data_exfiltration" and not case["protected_canaries"]:
            errors.append(f"line {line_number}: data_exfiltration case needs a protected canary")
        category_counts[case["category"]] += 1
    if not seen:
        errors.append("dataset is empty")
    if seen and category_counts["benign_control"] == 0:
        errors.append("dataset has no benign controls")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python -m aasb.validate PATH.jsonl", file=sys.stderr)
        return 2
    errors = validate(Path(sys.argv[1]))
    if errors:
        for error in errors: print(f"FAIL — {error}")
        return 1
    print(f"PASS — valid dataset: {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
