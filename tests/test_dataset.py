import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aasb.validate import validate


class DatasetTest(unittest.TestCase):
    def test_seed_dataset_is_valid(self):
        self.assertEqual(validate(ROOT / "data" / "v0.1" / "cases.jsonl"), [])

    def test_seed_dataset_has_ten_cases(self):
        lines = (ROOT / "data" / "v0.1" / "cases.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 10)


if __name__ == "__main__":
    unittest.main()
