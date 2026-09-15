import os
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aasb.validate import validate


class DatasetTest(unittest.TestCase):
    def test_seed_dataset_is_valid(self):
        self.assertEqual(validate(ROOT / "data" / "v0.1" / "cases.jsonl"), [])

    def test_calibration_dataset_has_thirty_cases(self):
        lines = (ROOT / "data" / "v0.1" / "cases.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 30)

    def test_categories_and_dialects_are_balanced(self):
        cases = [json.loads(line) for line in (ROOT / "data" / "v0.1" / "cases.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(set(Counter(case["category"] for case in cases).values()), {6})
        self.assertEqual(Counter(case["dialect"] for case in cases), {"msa": 10, "egyptian": 10, "gulf": 10})

    def test_all_cases_await_native_review(self):
        cases = [json.loads(line) for line in (ROOT / "data" / "v0.1" / "cases.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual({case["review_status"] for case in cases}, {"draft"})


if __name__ == "__main__":
    unittest.main()
