# Arabic Agent Safety Bench: development plan

Status: pre-alpha, 29 October 2026. This plan accompanies the `experimental/v0.2-draft` line, which differs from the default branch.

## Evidence and limits

- A local copy of the experimental version passed 23 Python unit tests with `python -B -m unittest discover -s tests -v`. The 24 files examined in that copy matched the experimental branch blobs at the time of comparison.
- Tests use synthetic fixtures and mocked local endpoints. They do not establish language quality, agent safety, model performance, or benchmark validity. Native-language reviews and a model baseline remain outstanding.
- The experimental dataset has a 30-case seed and a separate 300-case synthetic draft. Do not merge the dataset or report its count as reviewed cases.

## Ordered milestones

1. **Freeze the review contract.** Preserve dataset version, case IDs, source and review records; check the schema and the promotion rules on synthetic examples. Acceptance: reviewed output is separate from the draft and reproducible from the audit trail.
2. **Language and scenario review.** Recruit two independent qualified reviewers per candidate case as the existing contract requires; report coverage, disagreements and missing dialects. Acceptance: only cases meeting the existing approval and scoring rules are promoted, and unresolved disagreements remain visible.
3. **Calibrate the scorer.** On 20–30 reviewed cases, compare scorer decisions with independently documented human judgments, including benign controls and attacks. Acceptance: publish the comparison, failure examples and a justified threshold decision; do not invent a threshold in advance.
4. **Real model baseline.** Select an authorized local or explicitly approved provider and retain model/version, configuration, complete case coverage, raw responses and failures. Acceptance: repeatable scoring on the exact reviewed dataset with incomplete runs labeled incomplete; no general safety claim.
5. **Benchmark positioning.** Compare scope and methodology with publicly documented Arabic agent evaluations such as [Arabic Native Agent Bench](https://github.com/mirogate/arabic-native-agent-bench). Acceptance: a specific documented difference and limitations, without treating repository popularity as buyer demand.

## Stop conditions

Keep synthetic data labeled; do not include credentials or real targets. A successful unit test, fixture score, or draft case count is not evidence of a safe model or validated benchmark. Preserve the experimental line until its release criteria are met.

