# Docs

This directory holds the working contracts for modernizing `transorthogonal-linguistics`.

Current focus:
- Establish the project contracts before changing code.
- Modernize the codebase from Python 2 to Python 3.
- Add harnesses before refactoring behavior.

Documents:
- `PROJECT_CONTRACT.md`: current project boundaries, assets, and constraints.
- `PYTHON3_MODERNIZATION_CONTRACT.md`: Python 3 migration goals, acceptance criteria, and risks.
- `HARNESS_STRATEGY.md`: how behavior will be captured and verified during modernization.
- `DATA_CONTRACT.md`: checked-in data locations, invariants, and packaging rules.
- `HUMAN_INPUT.md`: questions that require a human answer. This file is only updated when a real decision is blocked on human input.

Working rule:
- Do not treat undocumented behavior as stable. If behavior matters, capture it in a harness or contract first.
