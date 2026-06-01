"""
system.py — PhiScalingValidator: Diamond interface for P38.

Orchestrates all sub-analysers and exposes the canonical API used by
the CLI, notebooks, and Zenodo record generation.
"""

from __future__ import annotations

import datetime
from typing import Any

from .phi_constants import PHI, PHI_CUBEROOT, V_RIG, V_CMB_DIPOLE
from .crep_scaling import CREPScalingAnalyzer
from .beta_scaling import BetaScalingAnalyzer
from .q4_scaling import Q4ScalingAnalyzer
from .vrig_scaling import VRIGScalingAnalyzer
from .eml_scaling import EMLScalingAnalyzer
from .null_hypothesis import evaluate_null_hypothesis

__all__ = ["PhiScalingValidator"]

_ZENODO_DOI = "10.5281/zenodo.17472834"


class PhiScalingValidator:
    """
    Diamond interface for Phi^(1/3) universal scaling validation (P38).

    Aggregates results from CREP Spectrum (P17-P30), beta-cluster (P32),
    Q4 entropy landscape, V_RIG derivation, and EML tree depth (P37).
    """

    def __init__(self) -> None:
        self._crep = CREPScalingAnalyzer()
        self._beta = BetaScalingAnalyzer()
        self._q4 = Q4ScalingAnalyzer()
        self._eml = EMLScalingAnalyzer()
        self._vrig = VRIGScalingAnalyzer()
        self._run_results: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def run_cycle(self, packages: range = range(17, 38)) -> dict[str, Any]:
        """
        Execute the full validation cycle across the given package range.

        Returns a dict with keys:
            phi_cuberoot, universality_score, confirmed_packages, phase_events,
            crep, beta, q4, vrig, eml
        """
        crep_summary = self._crep.summary()
        beta_summary = self._beta.summary()
        q4_summary = self._q4.summary()
        eml_summary = self._eml.summary()
        vrig = self._vrig.summary()

        # Collect per-domain confirmation flags
        domain_flags: dict[str, bool] = {
            "crep": crep_summary["confirmed"],
            "beta": beta_summary["confirmed"],
            "q4": q4_summary["confirmed"],
            "eml": eml_summary["confirmed"],
        }
        confirmed_packages = [k for k, v in domain_flags.items() if v]
        score = len(confirmed_packages) / len(domain_flags)

        phase_events = self._build_phase_events(crep_summary, eml_summary)

        result: dict[str, Any] = {
            "phi_cuberoot": PHI_CUBEROOT,
            "universality_score": score,
            "confirmed_packages": confirmed_packages,
            "phase_events": phase_events,
            "packages_range": list(packages),
            "crep": crep_summary,
            "beta": beta_summary,
            "q4": q4_summary,
            "vrig": vrig,
            "eml": eml_summary,
            "domain_flags": domain_flags,
        }
        self._run_results = result
        return result

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    def get_crep_state(self) -> dict[str, Any]:
        """Return CREP Spectrum analysis summary."""
        return self._crep.summary()

    def get_utac_state(self) -> dict[str, Any]:
        """Return UTAC (beta-cluster) analysis summary."""
        return self._beta.summary()

    def get_phase_events(self) -> list[dict[str, Any]]:
        """Return detected Phi-scaling phase events."""
        if self._run_results is None:
            self.run_cycle()
        return self._run_results["phase_events"]  # type: ignore[index]

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def phi_occurrences(self) -> dict[str, Any]:
        """
        Return confirmed Phi-scaling occurrences with p-values.

        Runs the full cycle if not already executed.
        """
        if self._run_results is None:
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
        if self._run_results is None:
            self.run_cycle()
        return float(self._run_results["universality_score"])  # type: ignore[index]

    def to_zenodo_record(self) -> dict[str, Any]:
        """Return a Zenodo-compatible metadata record for P38."""
        if self._run_results is None:
            self.run_cycle()
        r = self._run_results
        return {
            "title": (
                "phi-scaling-validator — Phi^(1/3) Universal Scaling Validator "
                "(GenesisAeon P38)"
            ),
            "doi": _ZENODO_DOI,
            "version": "0.1.0",
            "license": "MIT",
            "upload_type": "software",
            "description": (
                "Cross-domain validation of the Phi^(1/3) approx 1.174 universal "
                "scaling exponent across GenesisAeon Packages P17-P37. "
                "Tests beta-cluster ratios, CREP spectrum spacing, Q4 entropy "
                "landscape, and EML tree depth ratios."
            ),
            "creators": [
                {"name": "Johann Romer", "affiliation": "MOR Research Collective"}
            ],
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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_phase_events(
        self,
        crep_summary: dict[str, Any],
        eml_summary: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Identify discrete phase-transition events in the scaling data."""
        events: list[dict[str, Any]] = []

        # CREP phase event: confirmed Phi^(1/3) spacing
        if crep_summary["confirmed"]:
            events.append(
                {
                    "domain": "CREP",
                    "type": "phi_cuberoot_spacing",
                    "p_value": crep_summary["p_value"],
                    "mean_ratio": crep_summary["mean_ratio"],
                }
            )

        # EML phase event: tree depth convergence
        if eml_summary["confirmed"]:
            events.append(
                {
                    "domain": "EML",
                    "type": "depth_ratio_convergence",
                    "p_value": eml_summary["p_value"],
                    "mean_ratio": eml_summary["mean_ratio"],
                }
            )

        # V_RIG proximity event: within 2% of c*alpha/Phi prediction
        if abs(V_RIG - 1352.12) < 0.5:
            events.append(
                {
                    "domain": "VRIG",
                    "type": "phi_velocity_prediction",
                    "v_rig": V_RIG,
                    "expected": 1352.12,
                }
            )

        return events
