"""
phi_scaling — Φ^(1/3) Universal Scaling Validator (GenesisAeon P38).

Exports the primary validator class and the key constant.
"""

from .phi_constants import PHI, PHI_2_3, PHI_CUBEROOT, PHI_SQROOT, V_CMB_DIPOLE, V_RIG
from .system import PhiScalingValidator

__all__ = [
    "PHI",
    "PHI_CUBEROOT",
    "PHI_SQROOT",
    "PHI_2_3",
    "V_RIG",
    "V_CMB_DIPOLE",
    "PhiScalingValidator",
]

__version__ = "1.1.0"
