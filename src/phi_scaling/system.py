"""
system.py — PhiScalingValidator: Diamond interface for P38.

Orchestrates all sub-analysers and exposes the canonical API used by
the CLI, notebooks, and Zenodo record generation.
"""

from __future__ import annotations

import datetime
from importlib.metadata import version as pkg_version
from typing import Any

from diamond_setup.protocol import (
    CREPState,
    DiamondPackage,
    UTACState,
    ZenodoCreator,
    ZenodoRecord,
)

from .beta_scaling import BetaScalingAnalyzer
from .crep_scaling import CREPScalingAnalyzer
from .eml_scaling import EMLScalingAnalyzer
from .phi_constants import PHI_CUBEROOT, V_RIG
from .q4_scaling import Q4ScalingAnalyzer
from .vrig_scaling import VRIGScalingAnalyzer

__all__ = ["PhiScalingValidator"]

_ZENODO_DOI = "10.5281/zenodo.17472834"


class PhiScalingValidator(DiamondPackage):
    """
    Diamond interface for Phi^(1/3) universal scaling validation (P38).

    Aggregates results from CREP Spectrum (P17-P30), beta-cluster (P32),
    Q4 entropy landscape, V_RIG derivation, and EML tree depth (P37).
    """

    PACKAGE_ID: int = 38

    def __init__(self) -> None:
        super().__init__()
        self._crep = CREPScalingAnalyzer()
        self._beta = BetaScalingAnalyzer()
        self._q4 = Q4ScalingAnalyzer()
        self._eml = EMLScalingAnalyzer()
        self._vrig = VRIGScalingAnalyzer()
        self._packages = range(17, 38)
        self._run_results: dict[str, Any] = {}

    def run_cycle(self, packages: range | None = None) -> dict[str, Any]:
        """Execute the full validation cycle across the given package range."""
        if packages is not None:
            self._packages = packages
        return super().run_cycle()

    def _run_cycle(self) -> dict[str, Any]:
        crep_summary = self._crep.summary()
        beta_summary = self._beta.summary()
        q4_summary = self._q4.summary()
        eml_summary = self._eml.summary()
        vrig = self._vrig.summary()

        domain_flags: dict[str, bool] = {
            "crep": crep_summary["confirmed"],
            "beta": beta_summary["confirmed"],
            "q4": q4_summary["confirmed"],
            "eml": eml_summary["confirmed"],
        }
        confirmed_packages = [k for k, v in domain_flags.items() if v]
        score = len(confirmed_packages) / len(domain_flags)

        phase_events = self._collect_phase_events(crep_summary, eml_summary)

        self._run_results = {
            "phi_cuberoot": PHI_CUBEROOT,
            "universality_score": score,
            "confirmed_packages": confirmed_packages,
            "phase_events": phase_events,
            "packages_range": list(self._packages),
            "crep": crep_summary,
            "beta": beta_summary,
            "q4": q4_summary,
            "vrig": vrig,
            "eml": eml_summary,
            "domain_flags": domain_flags,
        }
        return self._run_results

    def _build_crep_state(self) -> CREPState:
        if not self._run_results:
            raise RuntimeError("CREP state unavailable before _run_cycle completes")
        crep = self._run_results["crep"]
        score = float(self._run_results["universality_score"])
        mean_ratio = float(crep["mean_ratio"])
        c_val = min(1.0, score)
        r_val = 1.0 - min(1.0, abs(mean_ratio - PHI_CUBEROOT))
        e_val = min(1.0, mean_ratio / PHI_CUBEROOT) if PHI_CUBEROOT > 0 else 0.5
        p_val = min(1.0, 1.0 - float(crep["p_value"]))
        return CREPState(C=c_val, R=r_val, E=e_val, P=p_val)

    def _build_utac_state(self) -> UTACState:
        if not self._run_results:
            raise RuntimeError("UTAC state unavailable before _run_cycle completes")
        beta = self._run_results["beta"]
        h_norm = float(self._run_results["universality_score"])
        mean_ratio = float(beta["mean_ratio"])
        h_star = min(1.0, mean_ratio / PHI_CUBEROOT) if PHI_CUBEROOT > 0 else 0.5
        k_eff = max(1e-6, PHI_CUBEROOT)
        return UTACState(H=h_norm, H_star=h_star, K_eff=k_eff)

    def _build_phase_events(self) -> list[dict[str, Any]]:
        if not self._run_results:
            return []
        return list(self._run_results.get("phase_events", []))

    def _build_zenodo_record(self) -> ZenodoRecord:
        return ZenodoRecord(
            title=(
                "phi-scaling-validator — Phi^(1/3) Universal Scaling Validator "
                "(GenesisAeon P38)"
            ),
            description=(
                "Cross-domain validation of the Phi^(1/3) approx 1.174 universal "
                "scaling exponent across GenesisAeon Packages P17-P37. "
                "Tests beta-cluster ratios, CREP spectrum spacing, Q4 entropy "
                "landscape, and EML tree depth ratios."
            ),
            creators=[
                ZenodoCreator(name="Römer, Johann", affiliation="MOR Research Collective"),
            ],
        )

    def phi_occurrences(self) -> dict[str, Any]:
        """Return confirmed Phi-scaling occurrences with p-values."""
        if not self._run_results:
            self.run_cycle()
        r = self._run_results
        return {
            "crep": {
                "confirmed": r["crep"]["confirmed"],
                "p_value": r["crep"]["p_value"],
                "mean_ratio": r["crep"]["mean_ratio"],
            },
            "beta": {
                "confirmed": r["beta"]["confirmed"],
                "p_value": r["beta"]["p_value"],
                "mean_ratio": r["beta"]["mean_ratio"],
            },
            "q4": {
                "confirmed": r["q4"]["confirmed"],
                "p_value": r["q4"]["p_value"],
                "mean_ratio": r["q4"]["mean_ratio"],
            },
            "eml": {
                "confirmed": r["eml"]["confirmed"],
                "p_value": r["eml"]["p_value"],
                "mean_ratio": r["eml"]["mean_ratio"],
            },
        }

    def universality_score(self) -> float:
        """Fraction of domains where Phi^(1/3) scaling is confirmed (p<0.05)."""
        if not self._run_results:
            self.run_cycle()
        return float(self._run_results["universality_score"])

    def to_zenodo_record(self) -> dict[str, Any]:
        """Return a Zenodo-compatible metadata record for P38."""
        if not self._run_results:
            self.run_cycle()
        r = self._run_results
        base = super().to_zenodo_record()
        return {
            **base,
            "doi": _ZENODO_DOI,
            "version": pkg_version("phi-scaling-validator"),
            "license": "MIT",
            "upload_type": "software",
            "keywords": [
                "golden ratio",
                "scaling exponent",
                "CREP",
                "UTAC",
                "complex systems",
                "criticality",
                "GenesisAeon",
            ],
            "related_identifiers": [
                {
                    "identifier": _ZENODO_DOI,
                    "relation": "isPartOf",
                    "scheme": "doi",
                }
            ],
            "results_summary": {
                "phi_cuberoot": r["phi_cuberoot"],
                "universality_score": r["universality_score"],
                "confirmed_domains": r["confirmed_packages"],
            },
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def _collect_phase_events(
        self,
        crep_summary: dict[str, Any],
        eml_summary: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Identify discrete phase-transition events in the scaling data."""
        events: list[dict[str, Any]] = []

        if crep_summary["confirmed"]:
            events.append({
                "domain": "CREP",
                "type": "phi_cuberoot_spacing",
                "p_value": crep_summary["p_value"],
                "mean_ratio": crep_summary["mean_ratio"],
            })

        if eml_summary["confirmed"]:
            events.append({
                "domain": "EML",
                "type": "depth_ratio_convergence",
                "p_value": eml_summary["p_value"],
                "mean_ratio": eml_summary["mean_ratio"],
            })

        if abs(V_RIG - 1352.12) < 0.5:
            events.append({
                "domain": "VRIG",
                "type": "phi_velocity_prediction",
                "v_rig": V_RIG,
                "expected": 1352.12,
            })

        return events