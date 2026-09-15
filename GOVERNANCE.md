# Governance

## Current phase

AASB is a maintainer-led pre-alpha project. This file describes the intended
decision process; it does not imply an existing external community.

## Decision priorities

1. Prevent real-world harm and disclosure of sensitive material.
2. Preserve dataset provenance and reproducibility.
3. Keep unsafe behavior and false refusals visible as separate outcomes.
4. Improve Arabic fidelity through documented native-language review.

Maintainers may reject material with uncertain ownership, real targets,
credentials, personal data, copied private prompts, or non-reproducible claims.
Security-sensitive reports should follow `SECURITY.md` rather than public issue
discussion.

## Dataset changes

Cases enter as `draft`. A case may become `native_reviewed` only through the
documented two-reviewer promotion workflow. Changing categories, expected
decisions, scoring denominators, or release thresholds requires a methodology
change and regression evidence.

## Releases

Versioned datasets are immutable after release. Corrections create a new
version and record affected case IDs; history is not silently rewritten.
