## Change type

- [ ] Original synthetic case(s)
- [ ] Validator, scorer, runner, or review tooling
- [ ] Documentation or methodology

## Evidence

Describe the observable change and paste the relevant local test command/output.
Do not include chain-of-thought, credentials, personal data, or private prompts.

## Required checks

- [ ] I ran `py -3.10 -m unittest discover -s tests -v`.
- [ ] New cases pass `aasb-validate`.
- [ ] New cases are original or have compatible explicit licensing.
- [ ] Tools, targets, identities, URLs, and secrets are synthetic.
- [ ] Dialect review remains `draft` unless two eligible native reviews exist.
- [ ] Claims distinguish fixtures, synthetic tests, and real model runs.
