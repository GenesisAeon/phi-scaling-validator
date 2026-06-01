"""
statistical_tests.py — Formal statistical tests for Φ^(1/3) universality.

All tests are honest, one-sample t-tests (or bootstrap) comparing observed
log-ratio means to the predicted value log(Φ^(1/3)) = log(Φ)/3.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np
import scipy.stats as stats

from .phi_constants import LOG_PHI_CUBEROOT, PHI, PHI_CUBEROOT

__all__ = [
    "TestResult",
    "test_phi_cuberoot_ratio",
    "test_geometric_spacing",
    "bootstrap_confidence_interval",
]


@dataclass
class TestResult:
    """Result of a one-sample hypothesis test for Φ-scaling."""

    statistic: float
    """t-statistic (or z-score for bootstrap)."""

    p_value: float
    """Two-tailed p-value."""

    confirmed: bool
    """True when p_value < 0.05 — null hypothesis rejected at 5 % level."""

    ci_95: tuple[float, float]
    """95 % confidence interval for the mean ratio (or log-ratio)."""

    n: int = 0
    """Number of observations."""

    mean_ratio: float = 0.0
    """Observed mean ratio."""

    expected_ratio: float = field(default_factory=lambda: PHI_CUBEROOT)
    """Expected ratio under Φ^(1/3) hypothesis."""

    note: str = ""
    """Human-readable summary."""

    @property
    def passes_frame_principle(self) -> bool:
        """True when |mean_ratio - expected_ratio| / expected_ratio ≤ 1/16."""
        return abs(self.mean_ratio - self.expected_ratio) / self.expected_ratio <= 1 / 16


def test_phi_cuberoot_ratio(
    ratios: Sequence[float],
    *,
    exponent: float = 1 / 3,
) -> TestResult:
    """
    One-sample t-test: do the *ratios* have mean equal to Φ^exponent?

    The test is performed on log-ratios (which linearises the multiplicative
    structure) and then back-transformed for reporting.

    Parameters
    ----------
    ratios:
        Sequence of positive ratio values r_i = x_{i+1} / x_i.
    exponent:
        Power of Φ to test against.  Defaults to 1/3.

    Returns
    -------
    TestResult
    """
    ratios_arr = np.asarray(ratios, dtype=float)
    if len(ratios_arr) < 2:
        raise ValueError("Need at least 2 ratios to run a t-test.")
    if np.any(ratios_arr <= 0):
        raise ValueError("All ratios must be strictly positive.")

    log_ratios = np.log(ratios_arr)
    mu0 = math.log(PHI) * exponent  # expected log-ratio under H0

    t_stat, p_val = stats.ttest_1samp(log_ratios, popmean=mu0)
    mean_log = float(np.mean(log_ratios))
    sem = float(stats.sem(log_ratios))
    ci_lo = mean_log - 1.96 * sem
    ci_hi = mean_log + 1.96 * sem
    mean_ratio = math.exp(mean_log)

    note = (
        f"n={len(ratios_arr)}, mean ratio={mean_ratio:.5f}, "
        f"expected Φ^({exponent:.4f})={PHI**exponent:.5f}, "
        f"t={t_stat:.3f}, p={p_val:.4f}"
    )

    return TestResult(
        statistic=float(t_stat),
        p_value=float(p_val),
        confirmed=float(p_val) < 0.05,
        ci_95=(math.exp(ci_lo), math.exp(ci_hi)),
        n=len(ratios_arr),
        mean_ratio=mean_ratio,
        expected_ratio=PHI**exponent,
        note=note,
    )


def test_geometric_spacing(
    values: Sequence[float],
    exponent: float = 1 / 3,
) -> TestResult:
    """
    Test whether sorted *values* are geometrically spaced with step Φ^exponent.

    Computes consecutive ratios of the sorted sequence then delegates to
    ``test_phi_cuberoot_ratio``.
    """
    arr = np.sort(np.asarray(values, dtype=float))
    if len(arr) < 2:
        raise ValueError("Need at least 2 values.")
    ratios = arr[1:] / arr[:-1]
    return test_phi_cuberoot_ratio(ratios.tolist(), exponent=exponent)


def bootstrap_confidence_interval(
    ratios: Sequence[float],
    n_boot: int = 10_000,
    *,
    seed: int = 42,
) -> tuple[float, float]:
    """
    Bootstrap 95 % CI for the mean ratio (geometric mean of ratios).

    Parameters
    ----------
    ratios:
        Positive ratio values.
    n_boot:
        Number of bootstrap resamples.
    seed:
        Random seed for reproducibility.

    Returns
    -------
    (lower_2.5%, upper_97.5%) on the *ratio* scale (not log scale).
    """
    rng = np.random.default_rng(seed)
    arr = np.asarray(ratios, dtype=float)
    log_arr = np.log(arr)
    boot_means = np.array(
        [rng.choice(log_arr, size=len(log_arr), replace=True).mean() for _ in range(n_boot)]
    )
    lo, hi = np.percentile(boot_means, [2.5, 97.5])
    return float(math.exp(lo)), float(math.exp(hi))
