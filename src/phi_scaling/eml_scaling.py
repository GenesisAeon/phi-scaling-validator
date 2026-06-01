"""
eml_scaling.py — Φ in EML operator tree depth ratios (P37 bridge).

The EML operator eml(x,y) = exp(x) - ln(y) generates all elementary
functions as binary trees.  Approximate tree depths for the main
GenesisAeon expressions are:

    tanh(σΓ)  → ~4 EML nodes
    CREP Γ    → ~6 EML nodes
    UTAC ODE  → ~8 EML nodes
    AFET Φ(H) → ~5 EML nodes
    v_RIG     → ~3 EML nodes

The claim: tree-depth ratios follow Φ^(1/3) spacing (tentative).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .phi_constants import PHI_CUBEROOT
from .statistical_tests import TestResult, test_phi_cuberoot_ratio

__all__ = [
    "EML_TREE_DEPTHS",
    "EMLScalingAnalyzer",
]


@dataclass(frozen=True)
class EMLExpression:
    name: str
    tree_depth: int
    """Approximate number of EML binary-tree nodes."""
    package: int


EML_TREE_DEPTHS: list[EMLExpression] = [
    EMLExpression("v_RIG",      3,  31),
    EMLExpression("tanh(σΓ)",   4,  17),
    EMLExpression("AFET Φ(H)",  5,  34),
    EMLExpression("CREP Γ",     6,  17),
    EMLExpression("UTAC ODE",   8,  17),
    EMLExpression("Full L",    10,  37),
]


class EMLScalingAnalyzer:
    """
    Tests whether sorted EML tree depths are geometrically spaced by Φ^(1/3).

    Tree depths are *estimates*; this test is exploratory and acknowledged
    as having low precision.
    """

    @property
    def depths(self) -> list[int]:
        return sorted(e.tree_depth for e in EML_TREE_DEPTHS)

    @property
    def consecutive_ratios(self) -> list[float]:
        d = self.depths
        return [d[i + 1] / d[i] for i in range(len(d) - 1)]

    def analyse(self) -> TestResult:
        return test_phi_cuberoot_ratio(self.consecutive_ratios)

    def summary(self) -> dict[str, Any]:
        res = self.analyse()
        return {
            "depths": self.depths,
            "ratios": self.consecutive_ratios,
            "mean_ratio": res.mean_ratio,
            "phi_cuberoot": PHI_CUBEROOT,
            "p_value": res.p_value,
            "confirmed": res.confirmed,
            "note": "exploratory — tree depths are approximate estimates",
        }
