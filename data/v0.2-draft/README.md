# v0.2 draft candidate

This dataset combines the 30-case v0.1 calibration seed with 270 deterministic,
original synthetic draft cases generated from 90 scenario specifications across
18 workflow contexts and three Arabic varieties.

It is **not a release dataset**. Every added rendering remains `draft`; dialect
fidelity, scenario realism, and cross-variety equivalence have not received the
required two independent native-language reviews. The generation source is
`tools/build_v02_draft.py`; edit that source and rebuild instead of hand-editing
the generated JSONL.

Target balance after generation:

- 300 total cases.
- 60 cases in each of five categories.
- 100 cases each labeled MSA, Egyptian Arabic, and Gulf Arabic.
