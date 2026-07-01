# Changelog

All notable changes to phi-scaling-validator are documented here.

## [Unreleased]

## [1.1.0] — 2026-07-01

### Changed
- `PhiScalingValidator` subclasses `diamond_setup.DiamondPackage`.
- `diamond-setup>=2.1.0` as runtime dependency; vendored `src/diamond_setup/` removed.
- `get_crep_state` / `get_utac_state` raise `NotConvergedError` before first `run_cycle`.
- UTAC keys: `{H, H_star, K_eff}`; CREP key `Gamma`.
- Removed bundled `diamond` CLI script (use `diamond-setup` package).

## [1.0.0] — 2026

### Added

- Standardized GenesisAeon ecosystem release tooling: `.zenodo.json`
  community metadata, `RELEASE_GUIDE.md`, `CONTRIBUTING.md`, issue/PR
  templates (`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`).

### Changed

- Promoted to v1.0.0 as part of the GenesisAeon ecosystem-wide 1.0.0
  milestone. No breaking changes to the public API or Diamond Interface
  (`run_cycle`, `get_crep_state`, `get_utac_state`, `get_phase_events`,
  `to_zenodo_record`) since 0.1.0.

## [0.1.0] — 2026-06-01

### Added — Package 38 (phi-scaling-validator)

- `phi_constants.py` — Phi, Phi^(1/3), sigma_Phi=1/16, v_RIG=c*alpha/Phi, CODATA 2018 alpha
- `crep_scaling.py` — Phi^(1/3) spacing test for 14 CREP Gamma-values (P17-P30)
- `beta_scaling.py` — Beta-cluster ratio test, 5 domain clusters from 78 threshold systems (P32)
- `q4_scaling.py` — Phi-scaling in Q4 4-bit entropy levels (exploratory)
- `vrig_scaling.py` — v_RIG = c*alpha/Phi ~= 1352 km/s as Phi-derived scale (P31 bridge)
- `eml_scaling.py` — Phi in EML operator tree depth ratios (P37 bridge)
- `statistical_tests.py` — Honest one-sample t-tests on log-ratios + bootstrap CI
- `null_hypothesis.py` — Uniform(1.0, 1.5) null distribution + explicit falsification
- `system.py` — PhiScalingValidator Diamond interface (run_cycle / get_crep_state / get_utac_state / get_phase_events / to_zenodo_record)
- `cli.py` — `phi-validate run / report / zenodo` CLI
- `data/crep_spectrum_p17_p30.yaml` — 14 CREP entries
- `data/beta_clusters_78systems.yaml` — 5 domain clusters
- `data/zenodo_metadata.yaml` — Zenodo record
- `.zenodo.json` — GitHub-Zenodo integration metadata
- `CITATION.cff` — CFF citation file
- 4 Jupyter notebooks covering Phi power atlas, scaling tests, universality, EML connection
- 23 passing tests

### Added — diamond-setup scaffolder (initial)

- `diamond scaffold` CLI for GenesisAeon-compatible project skeletons
- Templates: `minimal`, `genesis` (adds domains.yaml + entropy-table bridge)
- `diamond validate` project health checker
