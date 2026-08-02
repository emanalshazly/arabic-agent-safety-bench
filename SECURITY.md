# Security Policy

This project is a safety/red-teaming benchmark, which means it
intentionally contains attack-style prompts. A few ground rules keep
that from turning into an actual liability.

## What this dataset must never contain

- Real credentials, API keys, tokens, or passwords (including in
  examples or `tool_context` fields) — use obviously fake placeholders.
- Real personal data about any identifiable person.
- Leaked or reverse-engineered system prompts from other AI products.
- Working exploit code beyond what's needed to describe a test case
  (this bench tests *agent behavior*, not exploit development).

If you find any of the above in this repo, report it privately (see
below) rather than opening a public issue — that avoids amplifying
exposure while it gets removed.

## Reporting a problem

- **Sensitive data found in the repo** (real secrets/PII slipped into a
  test case): open a private GitHub Security Advisory on this repo, or
  email the maintainer directly. Do not open a public issue.
- **Bugs in the runner, validator, or baselines**: a normal public
  GitHub issue is fine.
- **A vulnerability in an agent/product you tested using this bench**:
  that's between you and that product's own disclosure process — this
  repo is the test harness, not a vulnerability database for products
  tested with it.

## Scope

This bench measures single-turn text-based prompt injection, data
exfiltration, tool-misuse, and multilingual-confusion resistance. It is
not a general security audit tool and passing it is not a safety
certification.
