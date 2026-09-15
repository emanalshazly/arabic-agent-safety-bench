# Arabic Agent Safety Bench (AASB)

An open, reproducible benchmark for evaluating whether tool-using AI agents
follow trusted task instructions when Arabic or bilingual untrusted content
contains conflicting requests.

**Status:** pre-alpha 30-case calibration dataset and local validator. All
language review statuses are still `draft`; no model baseline has been run.

## What v0.1 covers

- Modern Standard Arabic, Egyptian Arabic, and Gulf Arabic.
- Five scenario families: instruction override, data exfiltration, malicious
  tool use, multilingual confusion, and benign controls.
- Synthetic tools and fake secrets only. Cases must never contain operational
  credentials or target a real service.
- Both attack and benign cases, so blanket refusal is not treated as safety.

## Quick start

```powershell
py -3.10 -m pip install --no-deps -e .
aasb-validate data/v0.1/cases.jsonl
aasb-score --cases data/v0.1/cases.jsonl --responses tests/fixtures/perfect_responses.jsonl
py -3.10 -m unittest discover -s tests -v
```

Run a local Ollama model and then score the observable responses:

```powershell
aasb-run --cases data/v0.1/cases.jsonl --provider ollama --endpoint http://127.0.0.1:11434 --model MODEL_NAME --output runs/MODEL_NAME.responses.jsonl --metadata runs/MODEL_NAME.metadata.json
aasb-score --cases data/v0.1/cases.jsonl --responses runs/MODEL_NAME.responses.jsonl --output runs/MODEL_NAME.score.json
```

`MODEL_NAME` is intentionally not preselected. A run is evidence only when the
metadata says all requested cases completed. Provider credentials for remote
OpenAI-compatible endpoints must be supplied through `AASB_API_KEY`; remote
network use additionally requires the explicit `--allow-remote` flag.

## Native-language review station

Run the local review UI (bound to localhost only):

```powershell
aasb-review
```

Two distinct reviewers must approve a case and give both human dimensions at
least 4/5 before it can be promoted. Review events are append-only. Promotion
writes a separate dataset and never changes the source file:

```powershell
aasb-promote --cases data/v0.1/cases.jsonl --reviews reviews/native_reviews.jsonl --output review-output/cases.reviewed.jsonl --report review-output/promotion-report.jsonl
```

The station is tooling for review, not evidence that review has occurred.

## Dataset grain

One JSONL row is one agent scenario. The formal contract is
`schema/case.schema.json`. Each scenario states the trusted task,
untrusted content, available synthetic tools, forbidden actions, and expected
decision. The public dataset does not include hidden chain-of-thought or leaked
system prompts.

## Evaluation contract

An adapter should return one JSONL row per case:

```json
{"case_id":"aasb_0001","decision":"refuse_untrusted_instruction","tool_calls":[],"disclosed_canaries":[]}
```

`decision` is behavior-level output, not a request for private reasoning. See
`docs/ADAPTER_CONTRACT.md` and `schema/response.schema.json`.
The deterministic scorer reports decision accuracy, forbidden tool-call rate,
canary disclosure rate, safe-behavior rate, benign task completion, and case
coverage. Aggregate pass thresholds remain unset until the response contract is
calibrated on 20–30 reviewed cases.

## Limitations

- The first 30 cases are authored calibration fixtures, not a representative sample.
- Dialect labels require native-speaker review before the first public release.
- No claim of model safety, defense effectiveness, or market uniqueness is made.
- Thresholds are intentionally unset until a pilot produces evidence.

See [METHODOLOGY.md](METHODOLOGY.md), [CONTRIBUTING.md](CONTRIBUTING.md), and
[SECURITY.md](SECURITY.md). Project decisions and unfinished release gates are
documented in [GOVERNANCE.md](GOVERNANCE.md), [ROADMAP.md](ROADMAP.md), and
[docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).

## License

Code and the original synthetic v0.1 fixtures are released under MIT. Imported
or uncertain-provenance corpus files are explicitly excluded from this repo.
