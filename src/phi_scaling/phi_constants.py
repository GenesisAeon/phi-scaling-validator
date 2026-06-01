"""
phi_constants.py — All Φ-related constants and derived quantities.

The golden ratio Φ = (1 + √5) / 2 ≈ 1.6180339887 appears as a universal
scaling exponent across GenesisAeon packages P17–P37.  The cube-root Φ^(1/3)
≈ 1.17480502 is the primary inter-scale step observed in CREP Spectrum
spacing, β-cluster ratios, and EML tree depth ratios.
"""

from __future__ import annotations

import math

__all__ = [
    "PHI",
    "PHI_CUBEROOT",
    "PHI_SQROOT",
    "PHI_2_3",
    "SIGMA_PHI",
    "C_KM_S",
    "ALPHA",
    "V_RIG",
    "V_CMB_DIPOLE",
    "LOG_PHI",
    "LOG_PHI_CUBEROOT",
]

# ---------------------------------------------------------------------------
# Core golden-ratio constants
# ---------------------------------------------------------------------------

PHI: float = (1 + 5**0.5) / 2
"""Golden ratio Φ ≈ 1.6180339887."""

PHI_CUBEROOT: float = PHI ** (1 / 3)
"""Φ^(1/3) ≈ 1.17480502 — universal inter-scale step (P38 main claim)."""

PHI_SQROOT: float = PHI**0.5
"""Φ^(1/2) ≈ 1.27201965."""

PHI_2_3: float = PHI ** (2 / 3)
"""Φ^(2/3) ≈ 1.38047502."""

LOG_PHI: float = math.log(PHI)
"""ln(Φ) ≈ 0.48121182505960344."""

LOG_PHI_CUBEROOT: float = math.log(PHI_CUBEROOT)
"""ln(Φ^(1/3)) = ln(Φ)/3 ≈ 0.16040394."""

# ---------------------------------------------------------------------------
# Frame Principle / uncertainty bounds
# ---------------------------------------------------------------------------

SIGMA_PHI: float = 1 / 16
"""Frame Principle tolerance: ±1/16 ≈ ±0.0625 relative deviation."""

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------

C_KM_S: float = 299_792.458
"""Speed of light in km/s (exact by definition)."""

ALPHA: float = 1 / 137.035_999_084
"""Fine-structure constant α (CODATA 2018)."""

V_RIG: float = C_KM_S * ALPHA / PHI
"""
Resonance-Interface Group velocity V_RIG = c·α/Φ ≈ 1352.12 km/s.

Derived purely from fundamental constants; compared with V_CMB_DIPOLE as
an independent prediction of the GenesisAeon framework.
"""

V_CMB_DIPOLE: float = 369.82
"""CMB kinematic dipole amplitude (Planck 2018, km/s)."""
