"""
vrig_scaling.py — v_RIG as a Φ-derived velocity scale (P31 bridge).

v_RIG = c · α / Φ ≈ 1352.12 km/s

This module checks how v_RIG sits in the Φ-power hierarchy of velocity scales
and computes the ratio v_RIG / v_CMB_dipole to test for Φ-alignment.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .phi_constants import PHI, V_CMB_DIPOLE, V_RIG

__all__ = [
    "VRIGScalingAnalyzer",
    "VRIGPhiReport",
]


@dataclass
class VRIGPhiReport:
    v_rig: float
    v_cmb: float
    ratio: float
    """v_RIG / v_CMB_dipole."""
    phi_power_estimate: float
    """log(ratio) / log(Φ) — how many Φ-steps separate the two scales."""
    nearest_phi_power: float
    """Nearest integer or simple fraction of a Φ-power."""
    deviation_from_phi: float
    """Fractional deviation from nearest Φ-power."""
    note: str


class VRIGScalingAnalyzer:
    """
    Analyses v_RIG = c·α/Φ in the context of Φ-scaling.

    The ratio v_RIG / v_CMB ≈ 3.66.  log(3.66)/log(Φ) ≈ 2.69.
    The nearest simple Φ-power is Φ^(8/3) ≈ Φ^2.67 — close but not exact.
    This is reported transparently as a *suggestive* rather than confirmed
    Φ-relation.
    """

    def analyse(self) -> VRIGPhiReport:
        ratio = V_RIG / V_CMB_DIPOLE
        phi_power = np.log(ratio) / np.log(PHI)

        # Nearest simple Φ-power (check integer and third-integer powers)
        candidates = [round(phi_power * 3) / 3, round(phi_power)]
        best = min(candidates, key=lambda p: abs(p - phi_power))
        deviation = abs(phi_power - best) / max(abs(best), 1e-9)

        note = (
            f"v_RIG/v_CMB = {ratio:.4f} ≈ Φ^{phi_power:.3f}. "
            f"Nearest simple Φ-power: Φ^{best:.3f}. "
            f"Deviation: {deviation:.1%}. "
            "Result: suggestive, not a formal Φ^(1/3) confirmation."
        )

        return VRIGPhiReport(
            v_rig=V_RIG,
            v_cmb=V_CMB_DIPOLE,
            ratio=ratio,
            phi_power_estimate=float(phi_power),
            nearest_phi_power=float(best),
            deviation_from_phi=float(deviation),
            note=note,
        )

    def summary(self) -> dict:
        r = self.analyse()
        return {
            "v_rig_km_s": r.v_rig,
            "v_cmb_km_s": r.v_cmb,
            "ratio": r.ratio,
            "phi_power": r.phi_power_estimate,
            "nearest_phi_power": r.nearest_phi_power,
            "deviation": r.deviation_from_phi,
            "confirmed": False,  # suggestive only
            "note": r.note,
        }
