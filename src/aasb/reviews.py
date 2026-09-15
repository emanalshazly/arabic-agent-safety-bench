import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SCORE_FIELDS = ("interpretation_fidelity", "scenario_realism")

def load_jsonl(path):
    path = Path(path)
    if not path.exists(): return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def validate_review(review, case_ids):
    errors = []
    if review.get("case_id") not in case_ids: errors.append("unknown case_id")
    if not str(review.get("reviewer", "")).strip(): errors.append("reviewer is required")
    if review.get("decision") not in {"approve", "revise"}: errors.append("decision must be approve or revise")
    for field in SCORE_FIELDS:
        value = review.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
            errors.append(f"{field} must be an integer from 1 to 5")
    if not isinstance(review.get("notes", ""), str): errors.append("notes must be a string")
    return errors

def append_review(path, review, case_ids):
    errors = validate_review(review, case_ids)
    if errors: raise ValueError("; ".join(errors))
    normalized = {"case_id": review["case_id"], "reviewer": review["reviewer"].strip(),
        "interpretation_fidelity": review["interpretation_fidelity"], "scenario_realism": review["scenario_realism"],
        "decision": review["decision"], "notes": review.get("notes", "").strip(),
        "reviewed_at": datetime.now(timezone.utc).isoformat()}
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle: handle.write(json.dumps(normalized, ensure_ascii=False) + "\n")
    return normalized

def latest_reviews_by_case(reviews):
    latest = {}
    for review in reviews: latest[(review["case_id"], review["reviewer"].casefold())] = review
    grouped = defaultdict(list)
    for (case_id, _), review in latest.items(): grouped[case_id].append(review)
    return grouped

def promotion_reason(case_reviews, minimum_score=4):
    if len(case_reviews) < 2: return "needs_two_distinct_reviewers"
    if any(review["decision"] != "approve" for review in case_reviews): return "revision_requested"
    if any(review[field] < minimum_score for review in case_reviews for field in SCORE_FIELDS): return "score_below_minimum"
    return "eligible"

def promote_cases(cases, reviews, minimum_score=4):
    grouped = latest_reviews_by_case(reviews); promoted = []; report = []
    for case in cases:
        reason = promotion_reason(grouped.get(case["case_id"], []), minimum_score); updated = dict(case)
        if reason == "eligible": updated["review_status"] = "native_reviewed"
        promoted.append(updated); report.append({"case_id": case["case_id"], "status": updated["review_status"], "reason": reason})
    return promoted, report

def write_jsonl(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Create a reviewed derivative without changing the source dataset")
    parser.add_argument("--cases", required=True); parser.add_argument("--reviews", required=True)
    parser.add_argument("--output", required=True); parser.add_argument("--report", required=True)
    parser.add_argument("--minimum-score", type=int, default=4, choices=range(1, 6)); args = parser.parse_args()
    cases = load_jsonl(args.cases); promoted, report = promote_cases(cases, load_jsonl(args.reviews), args.minimum_score)
    write_jsonl(args.output, promoted); write_jsonl(args.report, report)
    count = sum(row["review_status"] == "native_reviewed" for row in promoted)
    print(f"promoted={count} pending={len(promoted) - count} output={args.output}")

if __name__ == "__main__": main()
