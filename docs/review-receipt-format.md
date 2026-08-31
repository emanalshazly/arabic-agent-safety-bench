# Native-language review receipt

Every reviewed batch must include this receipt in its pull request. The receipt is evidence of the named review action only; it is not a benchmark release or a model-quality result.

```yaml
review_receipt_version: 1
commit_sha: <full SHA reviewed>
reviewed_at_utc: <YYYY-MM-DDTHH:MM:SSZ>
reviewer_github_handle: <handle>
dialect_qualification: <msa|egyptian|gulf and short basis>
case_ids:
  - <case-id>
checks:
  natural_for_claimed_dialect: <pass|fail>
  expected_behavior_is_correct: <pass|fail>
  attack_or_control_is_plausible: <pass|fail>
  contains_no_real_secret_or_pii: <pass|fail>
  source_and_license_acceptable: <pass|fail>
notes: <required when any check fails>
decision: <approve|request_changes>
```

Rules:

- The reviewer must inspect the exact commit SHA recorded above.
- A contributor may not self-certify dialect expertise without stating its basis.
- `reviewed_by` is populated only for approved case IDs.
- Machine translation or an LLM review cannot substitute for the native-language reviewer.
- If no reviewer is available, retain an empty `reviewed_by` and record the batch as `BLOCKED`.
