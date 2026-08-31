## Scope

- [ ] Dataset cases
- [ ] Baseline or runner
- [ ] Documentation only

## Required checks

- [ ] `python scripts/validate_dataset.py`
- [ ] `python runner/cli.py --baseline regex`
- [ ] No real secrets, PII, or leaked prompts
- [ ] Source and license recorded for every added case

## Native review receipt

Required for every changed or added case. Paste the completed YAML from [`docs/review-receipt-format.md`](../docs/review-receipt-format.md), or state `BLOCKED — native reviewer unavailable`. Do not populate `reviewed_by` when blocked.

## Evidence boundary

Describe only checks actually run. CI and regex-baseline results do not establish native-language quality or model-backed safety performance.
