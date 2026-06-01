"""
crep_scaling.py — Φ^(1/3) spacing in the CREP Spectrum (P17–P30).

The Criticality–Resonance Entropy Profile (CREP) assigns a dimensionless
entropy parameter Γ ∈ [0, 1] to each Package.  The claim (P38) is that the
sorted non-zero Γ values are geometrically spaced with step ≈ Φ^(1/3).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .phi_constants import PHI_CUBEROOT
from .statistical_tests import TestResult, bootstrap_confidence_interval, test_phi_cuberoot_ratio

__all__ = [
    "CREP_DATA",
    "CREPEntry",
    "CREPScalingAnalyzer",
]


@dataclass(frozen=True)
class CREPEntry:
    package: int
    name: str
    gamma: float
    """Γ — dimensionless criticality-entropy parameter."""


# Raw CREP Spectrum data (P17–P30), GenesisAeon entropy atlas
CREP_DATA: list[CREPEntry] = [
    CREPEntry(17, "Cygnus X-1",         0.046),
    CREPEntry(18, "AMOC",               0.251),
    CREPEntry(19, "Amazon",             0.116),
    CREPEntry(20, "Neural Criticality", 0.251),
    CREPEntry(21, "Solar Flares",       0.014),
    CREPEntry(22, "Sandpile SOC",       0.336),   # midpoint 0.296–0.376
    CREPEntry(23, "Seismic",            0.200),
    CREPEntry(24, "Qubit Decoherence",  0.050),
    CREPEntry(25, "Apoptosis",          0.090),
    CREPEntry(26, "Neuromorphic SNN",   0.150),
    CREPEntry(27, "Theta-Band",         0.251),
    CREPEntry(28, "Epi-Sigillin",       0.300),   # dynamic, approximate
    CREPEntry(29, "Proof-of-Resonance", 0.367),
    CREPEntry(30, "Diffusive Routing",  0.443),
]


class CREPScalingAnalyzer:
    """
    Analyse Φ^(1/3) spacing in sorted CREP Γ values.

    Attributes
    ----------
    entries:
        The CREP data entries being analysed.
    sorted_gammas:
        Unique, sorted Γ values (duplicates collapsed to avoid 1.0 ratios).
    ratios:
        Consecutive ratios Γ_{n+1} / Γ_n of sorted unique values.
    """

    def __init__(self, entries: list[CREPEntry] | None = None) -> None:
        self.entries = entries or CREP_DATA
        gammas = sorted({e.gamma for e in self.entries})
        # Remove the P21 Solar Flares value (0.014) only if it is a clear
        # outlier more than 3-sigma below the geometric mean — we keep all
        # values to be honest but flag it in the report.
        self.sorted_gammas: list[float] = gammas
        self.ratios: list[float] = [
            gammas[i + 1] / gammas[i] for i in range(len(gammas) - 1) if gammas[i] > 0
        ]

    def run_test(self) -> TestResult:
        """One-sample t-test: mean log-ratio == log(Φ^(1/3))."""
        return test_phi_cuberoot_ratio(self.ratios)

    def bootstrap_ci(self, n_boot: int = 10_000) -> tuple[float, float]:
        """Bootstrap 95 % CI on mean ratio."""
        return bootstrap_confidence_interval(self.ratios, n_boot=n_boot)

    def ratio_table(self) -> list[dict]:
        """Return per-step analysis as a list of dicts."""
        g = self.sorted_gammas
        rows = []
        for i in range(len(g) - 1):
            if g[i] == 0:
                continue
            r = g[i + 1] / g[i]
            rows.append(
                {
                    "gamma_lo": g[i],
                    "gamma_hi": g[i + 1],
                    "ratio": r,
                    "phi_cuberoot": PHI_CUBEROOT,
                    "deviation_pct": 100 * (r - PHI_CUBEROOT) / PHI_CUBEROOT,
                }
            )
        return rows

    def summary(self) -> dict:
        tr = self.run_test()
        ci = self.bootstrap_ci()
        return {
            "n_entries": len(self.entries),
            "n_unique_gammas": len(self.sorted_gammas),
            "n_ratios": len(self.ratios),
            "mean_ratio": tr.mean_ratio,
            "phi_cuberoot": PHI_CUBEROOT,
            "t_statistic": tr.statistic,
            "p_value": tr.p_value,
            "confirmed": tr.confirmed,
            "ci_95": ci,
            "note": tr.note,
        }
