# Contributing

Thanks for helping build this out — the dataset is the whole point of
this project, so most contributions will be test cases.

## Adding a test case

1. Add one line to `data/test_cases.jsonl` following
   [`schema/test_case.schema.json`](schema/test_case.schema.json):
   - `id`: unique slug, `<category-short>-<dialect>-<number>`, e.g. `tool-misuse-egy-003`
   - `category`: one of `instruction_override`, `data_exfiltration`,
     `malicious_tool_use`, `multilingual_confusion`, `benign_control`
   - `dialect`: `msa`, `egyptian`, or `gulf`
   - `prompt`: the actual text — write it natively in the dialect, don't
     machine-translate an English attack pattern
   - `expected_behavior`: `refuse_or_deflect` for attack categories,
     `comply_normally` for `benign_control`
   - `source`: `team_authored`, `adapted:<origin>`, or `contributed:<your-github-handle>`
   - `license`: the license you're contributing this specific case under (default CC-BY-4.0)
2. Run `python scripts/validate_dataset.py` — it must pass before you open a PR.
3. Run `python runner/cli.py` to sanity-check nothing broke.
4. Open a PR. **A native speaker of the case's dialect must review it
   before merge** — if that's not you, say so in the PR description and
   tag someone who can. Once reviewed, the reviewer's handle goes in
   `reviewed_by`.

### What makes a good case

- **Attack categories**: realistic — something an actual user (or a
  malicious one) might plausibly type, not a contrived edge case no one
  would ever send.
- **`benign_control`**: should *look* borderline enough that a jumpy
  filter would refuse it, but be something a reasonable agent should
  just do. These cases are as important as the attacks — a bench that
  only measures refusal rate rewards agents that refuse everything.
- **`multilingual_confusion`**: real code-switching patterns, not just
  an English attack with a translated preamble.

### What we won't merge

- Machine-translated English jailbreak lists with no dialectal rework.
- Leaked or reverse-engineered system prompts from other products.
- Anything containing real PII, real credentials, or real API keys —
  including in `tool_context` examples. Simulate, don't use real data.
- Cases without a `source` and `license` you can actually stand behind.

## Adding a baseline

Baselines live in `baselines/`, one module per baseline, exposing a
`score(prompt: str) -> dict` function returning
`{flagged, matched_patterns_or_reasoning, confidence}`. Register it in
`BASELINES` in `runner/cli.py`. Document what it is and its limitations
in the README's Baselines table — don't claim it's stronger than it's
been shown to be.

## Reporting issues

Bugs in the runner/validator: open a GitHub issue as normal.
Security-relevant reports (e.g. a case that inadvertently contains real
sensitive data): see [SECURITY.md](SECURITY.md) instead of a public issue.
