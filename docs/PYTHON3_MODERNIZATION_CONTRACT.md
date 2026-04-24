# Python 3 Modernization Contract

## Objective

Upgrade the project from Python 2 to Python 3 without changing the intended semantics of the core algorithms beyond compatibility and correctness fixes required for modern runtimes.

## Primary Deliverables

- Python 3-compatible package modules.
- Python 3-compatible command-line entry behavior.
- Updated dependency strategy with obsolete pins removed.
- A verification harness that exercises the main flows against the bundled data.

## Compatibility Targets

Initial target:
- Python 3.10+

Nice-to-have if low cost:
- Python 3.11+
- Python 3.12+

## Required Code Changes

Expected categories of change:
- `print` statements to functions.
- `xrange` to `range`.
- `cPickle` to `pickle`.
- Python 2 import behavior to explicit package-safe imports.
- File loading behavior updated for modern NumPy defaults where needed.
- Small correctness fixes discovered during harnessing.

## Dependency Contract

Current root requirements are obsolete and over-pinned.

Implementation intent:
- Remove strict pins from old package versions.
- Keep dependencies minimal.
- Avoid adding heavyweight dependencies unless required by testing or packaging.

Because root-level edits are currently paused, this document is the contract only; the dependency changes happen in a later code phase.

## Behavioral Preservation Contract

The modernization pass should preserve:
- `Features` loading semantics from local `.npy` files.
- The return shapes and ordering semantics of `transorthogonal_words`.
- The return shapes and ordering semantics of `slerp_word_path`.
- Basic CLI usage of passing word pairs as positional arguments.

The modernization pass may change:
- Error messages where Python 3 behavior requires it.
- Logging and output formatting details if necessary for correctness or clarity.
- Internal structure needed to support tests and cleaner imports.

## Acceptance Criteria

The first modernization pass is complete when:
- The package imports under Python 3.
- The main modules compile under Python 3.
- The CLI runs for at least one representative word pair using bundled data.
- A harness verifies core output structure and key invariants.
- No root-level redesign is required to use the code locally.

## Known Risks

- NumPy string loading behavior may differ across versions.
- Relative imports in script execution may break when converted to package-safe imports.
- The old code may rely on accidental Python 2 behaviors not yet visible from static inspection.
- Numerical outputs may drift slightly across Python and NumPy versions.

## Decision Rule

When behavior differs between:
- "old implementation detail" and "clear intended algorithmic behavior"

prefer the intended algorithmic behavior, but record the deviation in the harness notes.
