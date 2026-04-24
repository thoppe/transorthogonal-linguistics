# AGENTS

## Repository Contract

This repository is being modernized from the last recorded git update, not from a newly invented baseline.

Baseline:
- Last git update date: `2015-06-26`
- Baseline commit: `be84eb75814d74c344979361b929d533dba4d7e2`

Interpretation rule:
- Treat the repository as a historical Python 2 project created and last updated in that baseline state.
- All modernization work must preserve the original project intent unless an explicit contract says otherwise.
- If behavior changes, document the reason and classify it as compatibility, correctness, or intentional redesign.

## Documentation Rule

Project contracts live under `docs/`.

Current contract set:
- `docs/PROJECT_CONTRACT.md`
- `docs/PYTHON3_MODERNIZATION_CONTRACT.md`
- `docs/HARNESS_STRATEGY.md`
- `docs/HUMAN_INPUT.md` when human decisions are required

## Human Input Rule

If work is blocked on a human decision:
- record the question in `docs/HUMAN_INPUT.md`
- keep the question concrete and decision-oriented
- do not silently invent product decisions when the contract is ambiguous

## Current Modernization Priority

Phase 1:
- modernize the codebase from Python 2 to Python 3
- add harnesses before broad refactoring
- avoid unnecessary root-level redesign during the first pass

## Change Control

During the current phase:
- prefer small, reversible changes
- preserve bundled data assets unless a contract says otherwise
- do not assume undocumented behavior is stable; capture it in a harness first
