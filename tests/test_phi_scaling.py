"""Tests for phi_scaling — Package 38: Phi^(1/3) Universal Scaling Validator."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_phi_cuberoot_value():
    from phi_scaling import PHI, PHI_CUBEROOT

    # Phi^(1/3): actual computed value ~= 1.17398...
    assert abs(PHI_CUBEROOT - PHI ** (1 / 3)) < 1e-12
    assert 1.173 < PHI_CUBEROOT < 1.176


def test_phi_value():
    from phi_scaling import PHI

    assert abs(PHI - 1.6180339887) < 1e-9


def test_v_rig_approx():
    from phi_scaling import V_RIG

    assert abs(V_RIG - 1352.12) < 0.5, f"V_RIG={V_RIG} not near 1352.12"


def test_phi_constants_consistency():
    from phi_scaling.phi_constants import PHI, PHI_2_3, PHI_CUBEROOT, PHI_SQROOT

    assert abs(PHI_CUBEROOT**3 - PHI) < 1e-12
    assert abs(PHI_SQROOT**2 - PHI) < 1e-12
    assert abs(PHI_2_3 ** (3 / 2) - PHI) < 1e-10


# ---------------------------------------------------------------------------
# Statistical tests
# ---------------------------------------------------------------------------


def test_test_result_dataclass():
    from phi_scaling.statistical_tests import TestResult

    tr = TestResult(
        statistic=1.5,
        p_value=0.03,
        confirmed=True,
        ci_95=(1.1, 1.25),
        n=10,
        mean_ratio=1.17,
    )
    assert tr.confirmed is True
    assert hasattr(tr, "passes_frame_principle")


def test_phi_cuberoot_ratio_mean_on_ideal_data():
    """Ratios equal to Phi^(1/3) should yield mean_ratio == Phi^(1/3) and confirmed=True."""
    from phi_scaling import PHI_CUBEROOT
    from phi_scaling.statistical_tests import test_phi_cuberoot_ratio

    # Slight variation to avoid zero-variance scipy edge case
    ratios = [PHI_CUBEROOT * (1 + 1e-9 * (i - 10)) for i in range(20)]
    result = test_phi_cuberoot_ratio(ratios)
    assert abs(result.mean_ratio - PHI_CUBEROOT) < 1e-6
    assert result.n == 20
    # CI should contain expected value -> confirmed
    assert result.confirmed is True


def test_phi_cuberoot_ratio_not_confirmed_on_wrong_data():
    """Ratios far from Phi^(1/3) (e.g. 2.0) should NOT be confirmed."""
    from phi_scaling.statistical_tests import test_phi_cuberoot_ratio

    ratios = [2.0] * 30
    result = test_phi_cuberoot_ratio(ratios)
    # CI around 2.0 will not contain Phi^(1/3) ~= 1.174
    assert result.confirmed is False


def test_bootstrap_ci_contains_mean():
    from phi_scaling import PHI_CUBEROOT
    from phi_scaling.statistical_tests import bootstrap_confidence_interval

    ratios = [PHI_CUBEROOT * (1 + 0.05 * (i % 3 - 1)) for i in range(15)]
    lo, hi = bootstrap_confidence_interval(ratios)
    mean = sum(ratios) / len(ratios)
    assert lo < mean < hi


# ---------------------------------------------------------------------------
# CREP scaling
# ---------------------------------------------------------------------------


def test_crep_data_length():
    from phi_scaling.crep_scaling import CREP_DATA

    assert len(CREP_DATA) == 14


def test_crep_analyser_runs():
    from phi_scaling.crep_scaling import CREPScalingAnalyzer

    analyzer = CREPScalingAnalyzer()
    result = analyzer.run_test()  # returns TestResult
    assert hasattr(result, "p_value")
    assert hasattr(result, "confirmed")
    assert 0.0 <= result.p_value <= 1.0
    summary = analyzer.summary()
    assert "n_entries" in summary
    assert "confirmed" in summary


# ---------------------------------------------------------------------------
# Beta scaling
# ---------------------------------------------------------------------------


def test_beta_clusters_defined():
    from phi_scaling.beta_scaling import BETA_CLUSTERS

    assert len(BETA_CLUSTERS) == 5


def test_beta_analyser_runs():
    from phi_scaling.beta_scaling import BetaScalingAnalyzer

    result = BetaScalingAnalyzer().run_test()
    assert result.n == 4  # 5 clusters -> 4 consecutive ratios
    assert hasattr(result, "confirmed")
    assert hasattr(result, "mean_ratio")


# ---------------------------------------------------------------------------
# PhiScalingValidator (Diamond interface)
# ---------------------------------------------------------------------------


def test_validator_instantiates():
    from phi_scaling import PhiScalingValidator

    assert PhiScalingValidator() is not None


def test_validator_run_cycle_keys():
    from phi_scaling import PhiScalingValidator

    result = PhiScalingValidator().run_cycle()
    for key in ("phi_cuberoot", "universality_score", "confirmed_packages", "phase_events"):
        assert key in result, f"Missing key: {key}"


def test_validator_phi_cuberoot_in_result():
    from phi_scaling import PHI_CUBEROOT, PhiScalingValidator

    result = PhiScalingValidator().run_cycle()
    assert abs(result["phi_cuberoot"] - PHI_CUBEROOT) < 1e-10


def test_validator_universality_score_range():
    from phi_scaling import PhiScalingValidator

    v = PhiScalingValidator()
    v.run_cycle()
    assert 0.0 <= v.universality_score() <= 1.0


def test_validator_get_crep_state():
    from phi_scaling import PhiScalingValidator

    v = PhiScalingValidator()
    v.run_cycle()
    state = v.get_crep_state()
    assert isinstance(state, dict)
    for key in ("C", "R", "E", "P", "Gamma"):
        assert key in state, f"Missing CREP state key: {key}"


def test_validator_get_utac_state():
    from phi_scaling import PhiScalingValidator

    v = PhiScalingValidator()
    v.run_cycle()
    state = v.get_utac_state()
    assert set(state.keys()) == {"H", "H_star", "K_eff"}


def test_validator_get_phase_events():
    from phi_scaling import PhiScalingValidator

    v = PhiScalingValidator()
    v.run_cycle()
    assert isinstance(v.get_phase_events(), list)


def test_to_zenodo_record():
    from phi_scaling import PhiScalingValidator

    record = PhiScalingValidator().to_zenodo_record()
    assert record["doi"] == "10.5281/zenodo.17472834"
    assert "GenesisAeon" in record["keywords"]
    assert record["version"] == "1.1.0"


def test_phi_occurrences_structure():
    from phi_scaling import PhiScalingValidator

    occ = PhiScalingValidator().phi_occurrences()
    for domain in ("crep", "beta", "q4", "eml"):
        assert domain in occ
        assert "confirmed" in occ[domain]
        assert "p_value" in occ[domain]


# ---------------------------------------------------------------------------
# Null hypothesis
# ---------------------------------------------------------------------------


def test_null_hypothesis_evaluate():
    from phi_scaling import PHI_CUBEROOT
    from phi_scaling.null_hypothesis import FalsificationResult, evaluate_null_hypothesis

    ratios = [PHI_CUBEROOT * (1 + 0.02 * (i % 5 - 2)) for i in range(20)]
    result = evaluate_null_hypothesis(ratios)
    assert isinstance(result, FalsificationResult)
    assert hasattr(result, "phi_confirmed")
    assert hasattr(result, "within_sigma_phi")
    assert isinstance(result.phi_confirmed, bool)


def test_null_hypothesis_class():
    from phi_scaling.null_hypothesis import NullHypothesis

    nh = NullHypothesis()
    assert abs(nh.mean - 1.25) < 1e-10
    assert nh.pdf(1.25) > 0
    assert nh.pdf(2.0) == 0.0
