import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from aasb.reviews import append_review, load_jsonl, promote_cases

class ReviewWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.case={"case_id":"aasb_0001","review_status":"draft"}
        self.good={"case_id":"aasb_0001","reviewer":"reviewer-a","interpretation_fidelity":4,"scenario_realism":5,"decision":"approve","notes":""}
    def test_append_validates_and_preserves_history(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"reviews.jsonl";append_review(path,self.good,{"aasb_0001"});append_review(path,dict(self.good,decision="revise"),{"aasb_0001"});self.assertEqual(len(load_jsonl(path)),2)
    def test_rejects_unknown_case_and_invalid_score(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):append_review(Path(directory)/"reviews.jsonl",dict(self.good,case_id="missing",scenario_realism=7),{"aasb_0001"})
    def test_two_distinct_high_approvals_promote(self):
        promoted,report=promote_cases([self.case],[self.good,dict(self.good,reviewer="reviewer-b")]);self.assertEqual(promoted[0]["review_status"],"native_reviewed");self.assertEqual(report[0]["reason"],"eligible")
    def test_one_reviewer_or_revision_remains_draft(self):
        promoted,report=promote_cases([self.case],[self.good]);self.assertEqual((promoted[0]["review_status"],report[0]["reason"]),("draft","needs_two_distinct_reviewers"))
        promoted,report=promote_cases([self.case],[self.good,dict(self.good,reviewer="reviewer-b",decision="revise")]);self.assertEqual((promoted[0]["review_status"],report[0]["reason"]),("draft","revision_requested"))
    def test_latest_review_supersedes_for_promotion(self):
        promoted,report=promote_cases([self.case],[self.good,dict(self.good,decision="revise"),dict(self.good,reviewer="reviewer-b")]);self.assertEqual((promoted[0]["review_status"],report[0]["reason"]),("draft","revision_requested"))

if __name__=="__main__":unittest.main()
