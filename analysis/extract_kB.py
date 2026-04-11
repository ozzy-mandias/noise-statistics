# extract_kB.py
#
# Extracts Boltzmann's constant k_B from the measured Johnson noise variance
# of the 1 MΩ resistor using the Nyquist relation:
#
#   <V_J^2> = 4 k_B T R delta_f
#
# The oscilloscope captures the amplified voltage V_out = (G_pre * G_2) * V_J,
# so the measured (corrected) variance is:
#
#   <V_out^2>_corrected = (G_pre * G_2)^2 * <V_J^2>
#
# Solving for <V_J^2> and substituting into the Nyquist relation:
#
#   k_B = <V_out^2>_corrected / ((G_pre * G_2)^2 * 4 * T * R * delta_f)
#
# The analog squarer module (which divides by 10 V) was bypassed -- variance
# is computed digitally from raw oscilloscope traces, so no 10 V scaling applies.
#
# Inputs:  one_M_corrected, one_M_std from calc_moments.py
# Outputs: k_B with uncertainty, percent error vs CODATA value

import math
from calc_moments import one_M_corrected, one_M_std

# ---------------------------------------------------------------------------
# Constants and parameters
# ---------------------------------------------------------------------------

# Gain chain: LLE preamp fixed gain * HLE main amp gain
G_PRE   = 600       # LLE preamp gain (6 x 100, fixed)
G_2     = 200       # HLE main amp gain used for 1 MOhm runs
G_TOTAL = G_PRE * G_2

# Temperature: average across the three 1 MOhm runs, read from folder names
# Run 1: 297.5 K, Run 2: 297.5 K, Run 3: 297.6 K
T = (297.5 + 297.5 + 297.6) / 3   # Kelvin

# Resistance
R = 1_000_000   # Ohms

# Noise-equivalent bandwidth (nominal, from TeachSpin manual Table, f1=100Hz, f2=100kHz)
DELTA_F = 110_961   # Hz

# CODATA 2018 value for comparison
K_B_CODATA = 1.380649e-23   # J/K

# ---------------------------------------------------------------------------
# k_B extraction
# ---------------------------------------------------------------------------

# Step 1: recover <V_J^2> from measured output variance
var_J = one_M_corrected / (G_TOTAL ** 2)

# Step 2: solve Nyquist relation for k_B
k_B = var_J / (4 * T * R * DELTA_F)

# ---------------------------------------------------------------------------
# Uncertainty propagation
#
# k_B = C * <V_out^2>_corrected, where C = 1 / (G_total^2 * 4 * T * R * delta_f)
# is treated as a constant (gain, T, R, delta_f uncertainties not propagated here).
# So sigma_kB / k_B = sigma_var / <V_out^2>_corrected
# ---------------------------------------------------------------------------
sigma_kB = k_B * (one_M_std / one_M_corrected)

# Percent error vs CODATA
percent_error = abs(k_B - K_B_CODATA) / K_B_CODATA * 100

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("k_B EXTRACTION -- 1 MΩ resistor, gain 200")
    print("=" * 60)
    print(f"  Corrected variance <V_out^2>:  {one_M_corrected:.6e} V^2")
    print(f"  Variance uncertainty:          {one_M_std:.6e} V^2")
    print(f"  G_total = G_pre x G_2:         {G_TOTAL}")
    print(f"  Temperature T:                 {T:.2f} K")
    print(f"  Resistance R:                  {R:.2e} Ohm")
    print(f"  ENBW delta_f:                  {DELTA_F:.0f} Hz")
    print(f"  <V_J^2>:                       {var_J:.6e} V^2")
    print()
    print(f"  k_B measured:  {k_B:.4e} +/- {sigma_kB:.4e} J/K")
    print(f"  k_B CODATA:    {K_B_CODATA:.4e} J/K")
    print(f"  Percent error: {percent_error:.2f}%")