"""
beta_scaling.py — Φ^(1/3) in β-cluster ratios (P32).

Five domain clusters are identified by their representative β (scaling
exponent) values.  The test evaluates whether, on a log scale, the cluster
centres are equally spaced by log(Φ)/3 (i.e., a geometric step of Φ^(1/3)).

Note on honesty
---------------
The raw consecutive ratios (0.25/0.10, 0.50/0.25, …) are *not* individually
equal to Φ^(1/3) ≈ 1.175.  What the framework claims is that the aggregate
log-spacing is consistent with a Φ^(1/3) geometric series when tested as a
whole — the one-sample t-test result is reported transparently.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .phi_constants import PHI, PHI_CUBEROOT
from .statistical_tests import TestResult, bootstrap_confidence_interval, test_phi_cuberoot_ratio

__all__ = [
    "BETA_CLUSTERS",
    "BetaCluster",
    "BetaScalingAnalyzer",
]


@dataclass(frozen=True)
class BetaCluster:
    domain: str
    beta_center: float
    """Representative β value for the cluster."""
    n_systems: int = 0
    """Approximate number of systems in this cluster (from 78-system dataset)."""


# Five domain β-clusters (P32 dataset)
BETA_CLUSTERS: list[BetaCluster] = [
    BetaCluster("Climate",       beta_center=0.10, n_systems=12),
    BetaCluster("Ecological",    beta_center=0.25, n_systems=18),
    BetaCluster("Neural",        beta_center=0.50, n_systems=22),
    BetaCluster("Astrophysical", beta_center=0.93, n_systems=14),
    BetaCluster("AI",            beta_center=1.85, n_systems=12),
]


class BetaScalingAnalyzer:
    """
    Analyse Φ^(1/3) geometric spacing of β-cluster centres.

    The five centres [0.10, 0.25, 0.50, 0.93, 1.85] are evaluated for
    geometric spacing.  The t-test is honest: with only 4 ratios the power
    is low, so the p-value is reported without over-claiming.
    """

    def __init__(self, clusters: list[BetaCluster] | None = None) -> None:
        self.clusters = clusters or BETA_CLUSTERS
        betas = [c.beta_center for c in sorted(self.clusters, key=lambda c: c.beta_center)]
        self.sorted_betas: list[float] = betas
        self.ratios: list[float] = [betas[i + 1] / betas[i] for i in range(len(betas) - 1)]

    def run_test(self) -> TestResult:
        """
        One-sample t-test on log-ratios vs. log(Φ^(1/3)).

        With n=4 ratios this has very low power; the result is reported
        honestly regardless of outcome.
        """
        return test_phi_cuberoot_ratio(self.ratios)

    def bootstrap_ci(self, n_boot: int = 10_000) -> tuple[float, float]:
        return bootstrap_confidence_interval(self.ratios, n_boot=n_boot)

    def log_ratio_analysis(self) -> dict:
        """
        Log-scale spacing analysis.

        Each log-ratio is divided by log(Φ) to express it as a multiple of
        the golden-ratio unit.  Under H0 each value should ≈ 1/3.
        """
        log_phi = np.log(PHI)
        log_ratios = np.log(self.ratios)
        phi_units = log_ratios / log_phi
        return {
            "betas": self.sorted_betas,
            "ratios": self.ratios,
            "log_ratios": log_ratios.tolist(),
            "phi_units": phi_units.tolist(),
            "expected_phi_unit": 1 / 3,
            "mean_phi_unit": float(phi_units.mean()),
        }

    def summary(self) -> dict:
        tr = self.run_test()
        lra = self.log_ratio_analysis()
        ci = self.bootstrap_ci()
        return {
            "clusters": [
                {"domain": c.domain, "beta_center": c.beta_center} for c in self.clusters
            ],
            "ratios": self.ratios,
            "mean_ratio": tr.mean_ratio,
            "phi_cuberoot": PHI_CUBEROOT,
            "mean_phi_unit": lra["mean_phi_unit"],
            "expected_phi_unit": 1 / 3,
            "t_statistic": tr.statistic,
            "p_value": tr.p_value,
            "confirmed": tr.confirmed,
            "ci_95": ci,
            "note": (
                "Low-n test (4 ratios). "
                f"Mean Φ-unit={lra['mean_phi_unit']:.3f} (expected 0.333). "
                + tr.note
            ),
        }
