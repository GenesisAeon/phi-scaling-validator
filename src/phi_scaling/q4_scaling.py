"""
q4_scaling.py — Φ-scaling in the Q4 entropy landscape.

The Q4 state machine encodes system states as 4-bit binary vectors (0000–1111).
Each state has an associated volume-entropy S_V proportional to its Hamming
weight.  This module tests whether the *ratios* of distinct S_V levels follow
Φ^(1/3) spacing.

Q4 entropy model
----------------
S_V(state) ∝ w + 1   where w = Hamming weight (number of 1-bits)

Distinct levels: w ∈ {0,1,2,3,4} → S_V ∈ {1, 2, 3, 4, 5} (unnormalised).

Consecutive ratios: 2/1=2.0, 3/2=1.5, 4/3=1.333, 5/4=1.25 — these converge
toward 1.0.  The claim is softer: when normalised by the maximum level the
*geometric mean* of ratios is compared to Φ^(1/3).
"""

from __future__ import annotations

from typing import Any

from dataclasses import dataclass

from .phi_constants import PHI_CUBEROOT
from .statistical_tests import TestResult, test_phi_cuberoot_ratio

__all__ = [
    "Q4State",
    "Q4ScalingAnalyzer",
    "Q4_ENTROPY_MAP",
]

_N_BITS = 4


@dataclass(frozen=True)
class Q4State:
    bits: str
    """4-bit string e.g. '0101'."""
    hamming: int
    s_v: float
    """Volume entropy S_V = hamming + 1 (unnormalised)."""


# Build the full 16-state map
Q4_ENTROPY_MAP: dict[str, Q4State] = {
    f"{i:04b}": Q4State(
        bits=f"{i:04b}",
        hamming=bin(i).count("1"),
        s_v=float(bin(i).count("1") + 1),
    )
    for i in range(16)
}


class Q4ScalingAnalyzer:
    """
    Test Φ^(1/3) scaling in Q4 entropy levels.

    The five distinct S_V levels (1,2,3,4,5) represent the five Hamming-
    weight classes.  Consecutive ratios are tested against Φ^(1/3).

    This is an *exploratory* test: with only 4 ratios the statistical power
    is low, and the result is reported as 'inconclusive' unless p < 0.05.
    """

    def __init__(self) -> None:
        self._levels = sorted({s.s_v for s in Q4_ENTROPY_MAP.values()})

    @property
    def entropy_levels(self) -> list[float]:
        return list(self._levels)

    @property
    def consecutive_ratios(self) -> list[float]:
        lvls = self._levels
        return [lvls[i + 1] / lvls[i] for i in range(len(lvls) - 1)]

    def analyse(self) -> TestResult:
        """
        One-sample t-test of consecutive S_V ratios vs Φ^(1/3).

        Expected to be *inconclusive* given n=4 ratios; reported honestly.
        """
        return test_phi_cuberoot_ratio(self.consecutive_ratios)

    def summary(self) -> dict[str, Any]:
        res = self.analyse()
        return {
            "levels": self._levels,
            "ratios": self.consecutive_ratios,
            "mean_ratio": res.mean_ratio,
            "phi_cuberoot": PHI_CUBEROOT,
            "p_value": res.p_value,
            "confirmed": res.confirmed,
            "note": "low power (n=4); result expected to be inconclusive",
        }
