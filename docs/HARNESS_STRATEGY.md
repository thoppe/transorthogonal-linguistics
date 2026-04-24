# Harness Strategy

## Purpose

The codebase currently has no tests and no executable specification. Before refactoring, we need a lightweight harness that tells us whether the modernization changed behavior materially.

## Harness Principles

- Capture the current behavior that matters to users.
- Prefer invariant-based checks over brittle full-output snapshots.
- Use the bundled `db/` assets as the primary test fixture.
- Keep the first harness simple enough to run locally without extra infrastructure.

## Phase 1 Harness Scope

The first harness should validate:
- The data files load successfully.
- Vocabulary and feature matrix lengths align.
- Known words can be looked up.
- Representative word pairs produce non-empty results.
- Returned arrays have matching lengths.
- Time values are ordered monotonically after result sorting.
- Endpoint behavior is preserved where applicable.

Representative word pairs:
- `boy man`
- `mind body`
- `sun moon`

## Proposed Harness Shape

Initial preference:
- `pytest` tests over the package APIs.

If script-level execution is needed:
- add a minimal CLI smoke test layer after the package API harness exists.

## What Not To Assert Yet

Avoid strict equality on:
- Full word lists
- Floating-point values
- Exact ranking positions across environments

Those checks are too brittle for a first Python 3 migration, especially with unpinned modern dependencies.

## Failure Policy

If the harness reveals a difference:
- classify it as import/runtime failure, data-contract failure, numerical drift, or semantic regression
- fix import/runtime failures immediately
- evaluate numerical drift against the documented algorithm before changing behavior
- record any unresolved semantic question in `HUMAN_INPUT.md`
