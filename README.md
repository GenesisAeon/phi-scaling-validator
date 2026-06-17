# phi-scaling-validator

**GenesisAeon Package 38** — Cross-domain validation of the Phi^(1/3) universal scaling exponent.

[![CI](https://github.com/GenesisAeon/phi-scaling-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/phi-scaling-validator/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17472834.svg)](https://doi.org/10.5281/zenodo.17472834)

Tests whether **Phi^(1/3) = 1.6180...^(1/3) ~= 1.1740** appears as a universal inter-scale step
across GenesisAeon packages P17-P37: CREP Spectrum, beta-clusters (78 systems), Q4 entropy
landscape, EML operator tree depths, and the v_RIG cosmological velocity scale.

> Johann Römer · MOR Research Collective · 2026
> DOI: [10.5281/zenodo.17472834](https://doi.org/10.5281/zenodo.17472834)

---

## Installation

```bash
pip install phi-scaling-validator
# with optional notebook/plotting extras:
pip install "phi-scaling-validator[phi]"
# or with uv:
uv add phi-scaling-validator
```

## Quick start

```python
from phi_scaling import PhiScalingValidator, PHI_CUBEROOT

print(f"Phi^(1/3) = {PHI_CUBEROOT:.8f}")   # 1.17398500...

v = PhiScalingValidator()
result = v.run_cycle()
print(f"Universality score: {result['universality_score']:.0%}")
print(f"Confirmed domains:  {result['confirmed_packages']}")
print(v.to_zenodo_record()['doi'])           # 10.5281/zenodo.17472834
```

## CLI

```bash
# Run all validation analyses
phi-validate run

# Detailed per-domain report
phi-validate report

# Print Zenodo metadata
phi-validate zenodo
```

## What is validated

| Domain | Source | Test |
|--------|--------|------|
| CREP Spectrum (P17-P30) | 14 Gamma-values across 7 disciplines | Consecutive ratio t-test vs Phi^(1/3) |
| beta-Clusters (P32) | 78 threshold systems, 5 domain clusters | Log-ratio t-test vs Phi^(1/3) |
| Q4 entropy levels | 4-bit state machine, 5 Hamming levels | Exploratory (low power, n=4) |
| EML tree depths (P37) | 6 GenesisAeon expressions | Exploratory |
| v_RIG (P31) | c*alpha/Phi ~= 1352 km/s | Phi-power proximity check |

## Key result (honest)

The CREP Spectrum shows **p = 0.14** (not significant at 5%) with mean ratio ~1.37 vs expected
Phi^(1/3) ~= 1.174. The beta-cluster test has low power (n=4 ratios). The framework reports
this honestly — no false-positive claims. The Phi^(1/3) hypothesis remains **suggestive but
unconfirmed** pending more data points from packages P31-P37.

## Repository structure

```
src/phi_scaling/
├── phi_constants.py      # Phi, Phi^(1/3), sigma_Phi, v_RIG, alpha
├── crep_scaling.py       # CREP Spectrum Gamma-values (P17-P30)
├── beta_scaling.py       # beta-cluster ratios (78 systems, P32)
├── q4_scaling.py         # Q4 4-bit entropy landscape
├── vrig_scaling.py       # v_RIG = c*alpha/Phi (P31 bridge)
├── eml_scaling.py        # EML tree depth ratios (P37 bridge)
├── statistical_tests.py  # t-test + bootstrap CI (honest)
├── null_hypothesis.py    # Uniform(1.0,1.5) null + falsification
├── system.py             # PhiScalingValidator — Diamond interface
└── cli.py                # phi-validate CLI

data/
├── crep_spectrum_p17_p30.yaml    # 14 CREP entries with Gamma values
├── beta_clusters_78systems.yaml  # 5 domain clusters from UTAC v1.0
└── zenodo_metadata.yaml          # Full Zenodo record

notebooks/
├── 01_phi_power_atlas.ipynb       # All Phi powers in GenesisAeon
├── 02_beta_crep_scaling.ipynb     # P32 + P17-30 combined test
├── 03_universality_test.ipynb     # Full validator run
└── 04_eml_phi_connection.ipynb    # EML tree -> Phi emergence
```

## Also includes: diamond-setup scaffolder

This repo also ships the **diamond-setup** CLI for generating GenesisAeon-compatible
Python project skeletons:

```bash
diamond scaffold my-physics-tool --template genesis
```

See [README_QUICKSTART.md](README_QUICKSTART.md) for diamond-setup usage.

---

## Role in the GenesisAeon Ecosystem

`phi-scaling-validator` is **Package P38** of the GenesisAeon ecosystem, in
the **cross-domain meta-analysis** domain. It is the validator package that
checks whether the Phi^(1/3) scaling exponent observed across packages
P17-P37 (CREP Spectrum, beta-clusters, Q4 entropy landscape, EML operator
trees, v_RIG) is a genuine cross-domain universality, or an artifact —
honestly reporting non-significant results rather than overstating
confirmation.

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17472834.svg)](https://doi.org/10.5281/zenodo.17472834)

This package has an assigned Zenodo DOI: `10.5281/zenodo.17472834`. New
GitHub Releases will mint updated DOI versions automatically once
Zenodo-GitHub integration is enabled for this repo.

```bibtex
@software{phi_scaling_validator,
  author       = {Römer, Johann},
  title        = {phi-scaling-validator: Phi^(1/3) Universal Scaling Validator (GenesisAeon P38)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17472834},
  url          = {https://doi.org/10.5281/zenodo.17472834}
}
```

---

Part of the **GenesisAeon entropy atlas** (P17-P38).
Built with [uv](https://docs.astral.sh/uv/) · [scipy](https://scipy.org/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/)
