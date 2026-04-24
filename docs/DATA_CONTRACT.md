# Data Contract

## Purpose

This project keeps its canonical embedding assets checked into the repository as package data. The code and harnesses assume these files are present locally.

## Asset Locations

- `transorthogonal_linguistics/data/features.npy`
- `transorthogonal_linguistics/data/vocab.npy`

## Required Invariants

- `features.npy` must load as a 2D NumPy array.
- `vocab.npy` must load as a 1D NumPy array.
- `features.npy.shape[0] == vocab.npy.shape[0]`.
- Row `n` of `features.npy` must correspond to token `n` of `vocab.npy`.
- Vocabulary entries must be usable as Python string keys in the in-memory lookup index.

## Current Observed Shape

Observed in the current checked-in baseline:
- `features.npy.shape == (56356, 300)`
- `features.npy.dtype == float32`
- `vocab.npy.shape == (56356,)`
- `vocab.npy.dtype` is a Unicode string array

These values are part of the current maintainer expectation, but the first four invariants above matter more than exact dimensions if the data is intentionally regenerated later.

## Change Rules

- Do not replace these files casually. They define the behavior users see from the bundled examples and tests.
- If the embeddings are regenerated or replaced, update this document and the harness expectations in `tests/`.
- Any change that breaks row-to-token alignment is a hard failure.
- If vocabulary normalization changes, record the migration reason and expected user-facing impact.

## Packaging Rule

The `.npy` files are package data and should ship with the module. Code should resolve them relative to the installed package, not the caller's working directory.
