import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from aasb.review_report import build_report


def review(case_id, reviewer, fidelity=4, realism=4, decision="approve"):
    return {"case_id":case_id,"reviewer":reviewer,"interpretation_fidelity":fidelity,"scenario_realism":realism,"decision":decision,"notes":""}


class ReviewReportTest(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {"case_id":"aasb_0001","dialect":"msa","category":"benign_control"},
            {"case_id":"aasb_0002","dialect":"egyptian","category":"data_exfiltration"},
            {"case_id":"aasb_0003","dialect":"gulf","category":"malicious_tool_use"},
        ]
    def test_reports_coverage_eligibility_and_agreement(self):
        reviews = [review("aasb_0001","a",4,5),review("aasb_0001","b",5,5),review("aasb_0002","a",3,4),review("aasb_0002","b",4,4),review("aasb_0003","a")]
        report = build_report(self.cases, reviews)
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["cases_with_two_reviewers"], 2)
        self.assertEqual(report["eligible_cases"], 1)
        self.assertEqual(report["decision_agreement_rate"], 1)
        self.assertEqual(report["score_agreement"]["interpretation_fidelity"]["mean_absolute_difference"], 1)
    def test_latest_event_per_reviewer_is_used(self):
        reviews = [review("aasb_0001","a"),review("aasb_0001","a",decision="revise"),review("aasb_0001","b")]
        report = build_report(self.cases, reviews)
        self.assertEqual(report["promotion_reasons"]["revision_requested"], 1)
        self.assertEqual(report["pairwise_comparisons"], 1)
    def test_invalid_events_are_visible_and_excluded(self):
        report = build_report(self.cases, [review("missing","a")])
        self.assertEqual(report["valid_review_event_count"], 0)
        self.assertEqual(report["invalid_review_events"][0]["errors"], ["unknown case_id"])

if __name__ == "__main__": unittest.main()
