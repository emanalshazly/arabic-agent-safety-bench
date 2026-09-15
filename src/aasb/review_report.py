from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from .reviews import SCORE_FIELDS, latest_reviews_by_case, load_jsonl, promotion_reason


def _rate(numerator, denominator):
    return numerator / denominator if denominator else None


def _breakdown(cases, grouped, field, minimum_score):
    result = {}
    buckets = defaultdict(list)
    for case in cases:
        buckets[case[field]].append(case)
    for value, rows in sorted(buckets.items()):
        two = sum(len(grouped.get(case["case_id"], [])) >= 2 for case in rows)
        eligible = sum(promotion_reason(grouped.get(case["case_id"], []), minimum_score) == "eligible" for case in rows)
        result[value] = {"case_count": len(rows), "two_reviewer_cases": two, "two_reviewer_coverage": _rate(two, len(rows)), "eligible_cases": eligible}
    return result


def build_report(cases, reviews, minimum_score=4):
    case_ids = {case["case_id"] for case in cases}
    invalid = []
    valid = []
    for index, review in enumerate(reviews, 1):
        errors = []
        if review.get("case_id") not in case_ids: errors.append("unknown case_id")
        if not str(review.get("reviewer", "")).strip(): errors.append("reviewer is required")
        if review.get("decision") not in {"approve", "revise"}: errors.append("invalid decision")
        for field in SCORE_FIELDS:
            value = review.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5: errors.append(f"invalid {field}")
        if errors: invalid.append({"event": index, "case_id": review.get("case_id"), "errors": errors})
        else: valid.append(review)
    grouped = latest_reviews_by_case(valid)
    reasons = Counter(promotion_reason(grouped.get(case["case_id"], []), minimum_score) for case in cases)
    decision_matches = 0
    pair_count = 0
    absolute_differences = Counter()
    exact_score_matches = Counter()
    for case_reviews in grouped.values():
        for left, right in combinations(case_reviews, 2):
            pair_count += 1
            decision_matches += left["decision"] == right["decision"]
            for field in SCORE_FIELDS:
                difference = abs(left[field] - right[field])
                absolute_differences[field] += difference
                exact_score_matches[field] += difference == 0
    two_reviewer_cases = sum(len(grouped.get(case["case_id"], [])) >= 2 for case in cases)
    any_review_cases = sum(bool(grouped.get(case["case_id"], [])) for case in cases)
    return {
        "status": "human_review_complete" if two_reviewer_cases == len(cases) and not invalid else "incomplete",
        "case_count": len(cases),
        "review_event_count": len(reviews),
        "valid_review_event_count": len(valid),
        "invalid_review_events": invalid,
        "cases_with_review": any_review_cases,
        "cases_with_two_reviewers": two_reviewer_cases,
        "two_reviewer_coverage": _rate(two_reviewer_cases, len(cases)),
        "eligible_cases": reasons["eligible"],
        "promotion_reasons": dict(sorted(reasons.items())),
        "pairwise_comparisons": pair_count,
        "decision_agreement_rate": _rate(decision_matches, pair_count),
        "score_agreement": {field: {"mean_absolute_difference": _rate(absolute_differences[field], pair_count), "exact_agreement_rate": _rate(exact_score_matches[field], pair_count)} for field in SCORE_FIELDS},
        "by_dialect": _breakdown(cases, grouped, "dialect", minimum_score),
        "by_category": _breakdown(cases, grouped, "category", minimum_score),
        "minimum_promotion_score": minimum_score,
        "agreement_target_status": "unset_measure_first",
    }


def main():
    parser = argparse.ArgumentParser(description="Summarize native-review coverage and inter-reviewer agreement")
    parser.add_argument("--cases", required=True); parser.add_argument("--reviews", required=True); parser.add_argument("--output", required=True)
    parser.add_argument("--minimum-score", type=int, default=4, choices=range(1, 6)); args = parser.parse_args()
    report = build_report(load_jsonl(args.cases), load_jsonl(args.reviews), args.minimum_score)
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"status={report['status']} coverage={report['two_reviewer_coverage']} eligible={report['eligible_cases']} invalid_events={len(report['invalid_review_events'])}")
    return 0 if not report["invalid_review_events"] else 1

if __name__ == "__main__": raise SystemExit(main())
