# Project Contract

## Current State

Repository contents observed at start:
- Python package: `transorthogonal_linguistics/`
- Data assets: `transorthogonal_linguistics/data/features.npy`, `transorthogonal_linguistics/data/vocab.npy`
- Root docs and metadata: `README.md`, `requirements.txt`

Current code characteristics:
- Written for Python 2.
- Uses script-style module entry points instead of modern packaging and CLI structure.
- Has no tests, no CI, and no explicit runtime contract.
- Bundles large NumPy assets directly in the repository.

## Functional Scope

The repository currently appears to support three user-facing capabilities:
- Load a word embedding matrix and aligned vocabulary from local `.npy` files.
- Compute a linear "transorthogonal" word path between two words.
- Compute a spherical interpolation (`slerp`) word path between two words.

## In-Scope For The First Modernization Pass

- Make the package run on a modern Python 3 interpreter.
- Preserve the existing numerical intent and command-line usage shape where reasonable.
- Replace Python 2-only constructs with Python 3 equivalents.
- Introduce a harness so modernization can be verified against current behavior.
- Relax or replace obsolete dependency pins during the implementation phase.

## Out Of Scope For The First Pass

- Rebuilding the embedding database.
- Changing the mathematical method.
- Redesigning the repository layout at the root level.
- Adding a web application or reviving the old Heroku deployment.
- Large API redesigns not required for Python 3 compatibility.

## Repository Constraints

- Root-level files should not be edited until explicitly approved.
- Contracts should live under `docs/`.
- Questions that require human decisions must be recorded in `docs/HUMAN_INPUT.md`.

## Data Contract

Assumed invariants for the bundled data:
- `transorthogonal_linguistics/data/features.npy` is a 2D NumPy array of embedding vectors.
- `transorthogonal_linguistics/data/vocab.npy` is a 1D NumPy array of tokens aligned by row index with `features.npy`.
- The code relies on index alignment between those two arrays.

These assumptions must be validated by the harness before depending on them.

See also:
- `docs/DATA_CONTRACT.md`
