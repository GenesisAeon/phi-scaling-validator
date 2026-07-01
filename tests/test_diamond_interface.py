"""Tests for the PhiScalingValidator Diamond-Template interface (Package 38)."""

from __future__ import annotations

import pytest
from diamond_setup.protocol import NotConvergedError
from diamond_setup.validation import validate_diamond_instance

from phi_scaling.system import PhiScalingValidator


@pytest.fixture(scope="module")
def validator() -> PhiScalingValidator:
    v = PhiScalingValidator()
    v.run_cycle()
    return v


def test_not_converged_before_run_cycle():
    pkg = PhiScalingValidator()
    with pytest.raises(NotConvergedError):
        pkg.get_crep_state()


def test_validate_diamond_instance():
    pkg = PhiScalingValidator()
    assert validate_diamond_instance(pkg) == []


def test_run_cycle_returns_dict():
    result = PhiScalingValidator().run_cycle()
    assert isinstance(result, dict)
    assert "phi_cuberoot" in result


def test_get_crep_state_keys(validator: PhiScalingValidator):
    state = validator.get_crep_state()
    assert set(state.keys()) == {"C", "R", "E", "P", "Gamma"}


def test_get_utac_state_keys(validator: PhiScalingValidator):
    state = validator.get_utac_state()
    assert set(state.keys()) == {"H", "H_star", "K_eff"}


def test_to_zenodo_record_structure(validator: PhiScalingValidator):
    record = validator.to_zenodo_record()
    for key in ("title", "description", "creators", "doi", "results_summary"):
        assert key in record