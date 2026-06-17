# Contributing

Thanks for your interest in contributing to this GenesisAeon ecosystem
package!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows).
3. Install in editable mode with dev dependencies:
   `pip install -e ".[dev]"`.
4. Run the test suite: `pytest`.

## Code style

- Format and lint with `ruff` (`ruff format`, `ruff check`).
- Type-check with `mypy` (this repo uses `strict = true`).
- Keep functions documented with docstrings.

## Diamond Interface

`PhiScalingValidator` (in `src/phi_scaling/system.py`) implements the
GenesisAeon Diamond Interface: `run_cycle`, `get_crep_state`,
`get_utac_state`, `get_phase_events`, `to_zenodo_record`. Any change to
these methods' signatures or return shapes is a **breaking change** and
requires a MAJOR version bump (see `RELEASE_GUIDE.md`).

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This package reports statistical tests (t-test + bootstrap CI) on the
Phi^(1/3) scaling hypothesis with an explicit null hypothesis and
falsification conditions. If your contribution touches the statistical
methodology or the underlying data (`data/*.yaml`), please:
- Cite the source of any new data points.
- Clearly mark speculative vs. validated claims, consistent with the
  "Key result (honest)" section in `README.md`.
