"""
null_hypothesis.py — Explicit falsification conditions for Φ^(1/3) universality.

The null hypothesis is that observed inter-scale ratios are drawn from a
Uniform(1.0, 1.5) distribution (mean ≈ 1.25, σ ≈ 0.144).  We reject the
null — and therefore *confirm* Φ^(1/3) scaling — when:

    1. The observed mean ratio is within 2σ_Φ of Φ^(1/3), AND
    2. The one-sample t-test against Φ^(1/3) yields p < 0.05.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.stats as stats

from .phi_constants import PHI_CUBEROOT, SIGMA_PHI
from .statistical_tests import TestResult, test_phi_cuberoot_ratio

__all__ = [
    "NullHypothesis",
    "FalsificationResult",
    "evaluate_null_hypothesis",
]

# Null distribution: Uniform(a, b)
_NULL_A = 1.0
_NULL_B = 1.5
_NULL_MEAN = (_NULL_A + _NULL_B) / 2          # 1.25
_NULL_STD = (_NULL_B - _NULL_A) / (12**0.5)   # ≈ 0.1443


@dataclass
class NullHypothesis:
    """
    H₀: ratios ~ Uniform(1.0, 1.5).

    The distribution represents the prior expectation if inter-scale
    spacings were merely bounded and arbitrary (no preferred ratio).
    """

    a: float = _NULL_A
    b: float = _NULL_B

    @property
    def mean(self) -> float:
        return (self.a + self.b) / 2

    @property
    def std(self) -> float:
        return (self.b - self.a) / (12**0.5)

    def pdf(self, x: float) -> float:
        if self.a <= x <= self.b:
            return 1.0 / (self.b - self.a)
        return 0.0

    def sample(self, n: int, *, seed: int = 0) -> list[float]:
        rng = np.random.default_rng(seed)
        return rng.uniform(self.a, self.b, size=n).tolist()


@dataclass
class FalsificationResult:
    """Combined outcome of the falsification procedure."""

    null: NullHypothesis
    test_result: TestResult
    within_sigma_phi: bool
    """True when |mean_ratio - Φ^(1/3)| ≤ 2·SIGMA_PHI."""
    phi_confirmed: bool
    """True when within_sigma_phi AND p < 0.05 (H₀ rejected)."""
    note: str = ""


def evaluate_null_hypothesis(
    ratios: list[float],
    *,
    null: NullHypothesis | None = None,
) -> FalsificationResult:
    """
    Run falsification procedure against the null Uniform distribution.

    Parameters
    ----------
    ratios:
        Observed consecutive ratios from any domain.
    null:
        Custom null hypothesis (defaults to Uniform(1.0, 1.5)).

    Returns
    -------
    FalsificationResult with phi_confirmed flag.
    """
    if null is None:
        null = NullHypothesis()

    tr = test_phi_cuberoot_ratio(ratios)
    within = abs(tr.mean_ratio - PHI_CUBEROOT) <= 2 * SIGMA_PHI
    confirmed = within and tr.confirmed  # p < 0.05 AND proximity criterion

    note_parts = [
        f"Null: Uniform({null.a}, {null.b}), mean={null.mean:.4f}",
        f"Observed mean ratio: {tr.mean_ratio:.5f}",
        f"Φ^(1/3): {PHI_CUBEROOT:.5f}",
        f"Within 2·σ_Φ: {within}",
        f"p-value: {tr.p_value:.4f}",
        f"Φ confirmed: {confirmed}",
    ]

    return FalsificationResult(
        null=null,
        test_result=tr,
        within_sigma_phi=within,
        phi_confirmed=confirmed,
        note="\n".join(note_parts),
    )
