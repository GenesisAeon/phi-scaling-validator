# phi-scaling-validator

**GenesisAeon Package 38** — Cross-domain validation of the Phi^(1/3) universal scaling exponent.

DOI: [10.5281/zenodo.17472834](https://doi.org/10.5281/zenodo.17472834) · Johann Römer · MOR Research Collective · 2026

## What this package does

Tests whether **Phi^(1/3) ~= 1.1740** is a universal inter-scale step across the GenesisAeon
entropy atlas (P17-P37). The golden ratio cube root appears as a candidate structural constant
linking CREP Spectrum levels, beta-cluster domain boundaries, and EML operator tree depths.

## Quickstart

```bash
pip install "phi-scaling-validator[phi]"
```

```python
from phi_scaling import PhiScalingValidator, PHI_CUBEROOT

v = PhiScalingValidator()
result = v.run_cycle()
print(result['universality_score'])    # fraction of confirmed domains
print(v.to_zenodo_record()['doi'])     # 10.5281/zenodo.17472834
```

```bash
phi-validate run      # CLI: full validation report
phi-validate zenodo   # CLI: print Zenodo metadata
```

## GenesisAeon CREP Spectrum (P17-P30)

| Package | Name | Gamma |
|---------|------|-------|
| P17 | Cygnus X-1 Jet | 0.046 |
| P18 | AMOC | 0.251 |
| P19 | Amazon | 0.116 |
| P20 | Neural Criticality | 0.251 |
| P21 | Solar Flares | 0.014 |
| P22 | Sandpile SOC | 0.336 |
| P23 | Seismic | 0.200 |
| P29 | Proof-of-Resonance | 0.367 |
| P30 | Diffusive Routing | 0.443 |
| **P38** | **phi-scaling-validator** | **meta** |

Triple universality: AMOC = Neural Criticality = Theta-Band = Gamma ~= 0.251

## Also in this repo: diamond-setup

The `diamond` CLI scaffolds new GenesisAeon-compatible Python projects.
See [CLI Reference](cli.md) for both `diamond` and `phi-validate` commands.
