import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from aasb.validate import validate

class DraftExpansionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_v02_draft.py")], check=True, capture_output=True, text=True)
        cls.path = ROOT / "data" / "v0.2-draft" / "cases.jsonl"
        cls.cases = [json.loads(line) for line in cls.path.read_text(encoding="utf-8").splitlines()]
    def test_generated_dataset_is_schema_valid(self):
        self.assertEqual(validate(self.path), [])
    def test_target_size_and_balance(self):
        self.assertEqual(len(self.cases), 300)
        self.assertEqual(Counter(case["dialect"] for case in self.cases), {"msa":100,"egyptian":100,"gulf":100})
        self.assertEqual(set(Counter(case["category"] for case in self.cases).values()), {60})
    def test_ids_and_text_pairs_are_unique(self):
        self.assertEqual(len({case["case_id"] for case in self.cases}), 300)
        self.assertEqual(len({(case["trusted_task"],case["untrusted_content"]) for case in self.cases}), 300)
    def test_expansion_is_explicitly_unreviewed(self):
        self.assertEqual({case["review_status"] for case in self.cases}, {"draft"})

if __name__ == "__main__": unittest.main()
