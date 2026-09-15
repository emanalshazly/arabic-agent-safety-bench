import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aasb.score import load_jsonl, score


class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.cases = load_jsonl(ROOT / "data" / "v0.1" / "cases.jsonl")

    def test_perfect_fixture(self):
        responses = load_jsonl(ROOT / "tests" / "fixtures" / "perfect_responses.jsonl")
        result = score(self.cases, responses)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["coverage_rate"], 1.0)
        self.assertEqual(result["decision_accuracy"], 1.0)
        self.assertEqual(result["safe_behavior_rate"], 1.0)
        self.assertEqual(result["forbidden_tool_call_rate"], 0.0)
        self.assertEqual(result["canary_disclosure_rate"], 0.0)
        self.assertEqual(result["benign_task_completion_rate"], 1.0)

    def test_unsafe_fixture_detects_failures(self):
        responses = load_jsonl(ROOT / "tests" / "fixtures" / "unsafe_responses.jsonl")
        result = score(self.cases, responses)
        self.assertEqual(result["errors"], [])
        self.assertGreater(result["forbidden_tool_call_rate"], 0.0)
        self.assertGreater(result["canary_disclosure_rate"], 0.0)
        self.assertAlmostEqual(result["forbidden_tool_call_rate"], 24 / 26)
        self.assertEqual(result["canary_disclosure_rate"], 1.0)
        self.assertEqual(result["benign_task_completion_rate"], 0.0)

    def test_missing_response_is_reported(self):
        result = score(self.cases, [])
        self.assertEqual(result["evaluated_count"], 0)
        self.assertEqual(len(result["errors"]), len(self.cases))


if __name__ == "__main__":
    unittest.main()
