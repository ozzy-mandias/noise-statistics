# extract_kB.py
#
# Extracts Boltzmann's constant from the slope-unity fit of
# <V_J^2>/delta_f  vs  R  on log-log axes.
#
# The Nyquist relation gives:
#
#   <V_J^2> = 4 k_B T R delta_f
#
# Dividing both sides by delta_f:
#
#   <V_J^2> / delta_f = 4 k_B T * R
#
# On a log-log plot this is a line of slope 1 with intercept 4 k_B T.
# Fitting y = A * R (slope fixed to 1) gives  k_B = A / (4T).
#
# The fit uses 10 Ohm through 10 kOhm, where the PSD is flat and RC
# rolloff is negligible.  1 MOhm is plotted but excluded from the fit
# (RC rolloff reduces effective bandwidth).  100 kOhm is pending data
# collection.
#
# <V_J^2> is the baseline-corrected variance referred to the input:
#   <V_J^2> = <V_out^2>_corrected / G_total^2
#
# Inputs:  results list from calc_moments.py
# Outputs: k_B with uncertainty, plots/kB_extraction.png

import math
import numpy as np
import matplotlib.pyplot as plt
from calc_moments import results


# ============================================================================
# CONSTANTS
# ============================================================================

K_B_CODATA = 1.380649e-23   # J/K
DELTA_F    = 110_961         # Hz, noise-equivalent bandwidth
G1         = 600             # LLE preamp gain (fixed)

# Per-resistor parameters not stored in results
#   (R, G2, T_kelvin)
resistor_params = {
    10:      (300, (294.1 + 294.1 + 294.2) / 3),
    100:     (300, (294.6 + 294.6 + 294.6) / 3),
    1000:    (300, (294.7 + 294.7 + 294.8) / 3),
    10000:   (300, (294.8 + 294.6 + 294.7) / 3),
    1000000: (200, (297.5 + 297.5 + 297.6) / 3),
}


# ============================================================================
# COMPUTE  y = <V_J^2> / delta_f  FOR EACH RESISTOR
# ============================================================================

# results tuple: (R, corrected_var, std, mean_var, skew, skew_std, kurt, kurt_std)

data = []
for row in results:
    R          = row[0]
    corr_out   = row[1]   # baseline-corrected output variance (V^2)
    std_out    = row[2]   # run-to-run std of output variance
    G2, T      = resistor_params[R]
    G_total    = G1 * G2

    var_J      = corr_out / G_total**2          # input-referred Johnson variance
    sigma_varJ = std_out  / G_total**2

    y          = var_J   / DELTA_F              # <V_J^2> / delta_f
    sigma_y    = sigma_varJ / DELTA_F

    data.append({'R': R, 'y': y, 'sigma_y': sigma_y, 'T': T,
                 'G_total': G_total, 'var_J': var_J})


# ============================================================================
# WEIGHTED FIT:  y = A * R  (slope = 1 on log-log)
#
# Fit only 10 Ohm through 10 kOhm.
#   A = sum(w_i * y_i * R_i) / sum(w_i * R_i^2)
#   sigma_A = 1 / sqrt(sum(w_i * R_i^2))
# where w_i = 1 / sigma_y_i^2
# ============================================================================

fit_points = [d for d in data if d['R'] <= 10000]
T_avg = np.mean([d['T'] for d in fit_points])

R_fit     = np.array([d['R']       for d in fit_points])
y_fit     = np.array([d['y']       for d in fit_points])
sig_fit   = np.array([d['sigma_y'] for d in fit_points])

w = 1.0 / sig_fit**2
A       = np.sum(w * y_fit * R_fit) / np.sum(w * R_fit**2)
sigma_A = 1.0 / np.sqrt(np.sum(w * R_fit**2))


# ============================================================================
# k_B EXTRACTION
# ============================================================================

k_B_measured = A / (4.0 * T_avg)
sigma_kB     = sigma_A / (4.0 * T_avg)
pct_agree    = abs(k_B_measured - K_B_CODATA) / K_B_CODATA * 100


# ============================================================================
# OUTPUT AND PLOT (guarded)
# ============================================================================

if __name__ == '__main__':

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------
    print("=" * 62)
    print("k_B EXTRACTION — SLOPE METHOD")
    print("=" * 62)
    print(f"  Fit: <V_J^2>/delta_f = A * R,  slope fixed to 1 (log-log)")
    print(f"  Fit range: 10 Ohm to 10 kOhm")
    print(f"  A = {A:.4e} +/- {sigma_A:.4e} V^2/(Hz*Ohm)")
    print(f"  T (average of fit points): {T_avg:.2f} K")
    print(f"  delta_f (NEBW): {DELTA_F} Hz")
    print()
    print(f"  k_B measured:  {k_B_measured:.6e} +/- {sigma_kB:.6e} J/K")
    print(f"  k_B CODATA:    {K_B_CODATA:.6e} J/K")
    print(f"  Agreement:     {pct_agree:.2f}%")
    print()

    print("  Per-resistor data:")
    for d in data:
        tag = " *" if d['R'] > 10000 else ""
        print(f"    R = {d['R']:>10,.0f} Ohm   "
              f"<V_J^2>/df = {d['y']:.4e} +/- {d['sigma_y']:.4e}{tag}")
    print("  (* excluded from fit)")

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5.5))

    # Separate fit points from excluded points
    R_all   = np.array([d['R']       for d in data])
    y_all   = np.array([d['y']       for d in data])
    sig_all = np.array([d['sigma_y'] for d in data])

    fit_mask = R_all <= 10000
    exc_mask = ~fit_mask

    # Plot fit points
    ax.errorbar(R_all[fit_mask], y_all[fit_mask], yerr=sig_all[fit_mask],
                fmt='o', color='#2166ac', markersize=7, capsize=4,
                capthick=1.2, elinewidth=1.2, zorder=5,
                label='Fit data (10 Ω – 10 kΩ)')

    # Plot excluded points
    if np.any(exc_mask):
        ax.errorbar(R_all[exc_mask], y_all[exc_mask], yerr=sig_all[exc_mask],
                    fmt='s', color='#b2182b', markersize=7, capsize=4,
                    capthick=1.2, elinewidth=1.2, zorder=5,
                    label='Excluded (RC rolloff)')

    # Fit line spanning full R range
    R_line = np.logspace(0, 7, 500)
    ax.plot(R_line, A * R_line, '-', color='#2166ac', linewidth=1.2,
            alpha=0.7, zorder=3,
            label=r'Fit: $\langle V_J^2\rangle / \Delta f = 4k_BT \cdot R$')

    # Expected line (CODATA)
    A_codata = 4 * K_B_CODATA * T_avg
    ax.plot(R_line, A_codata * R_line, '--', color='gray', linewidth=1.0,
            alpha=0.6, zorder=2, label='CODATA prediction')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'Resistance $R$ (Ω)', fontsize=12)
    ax.set_ylabel(r'$\langle V_J^2 \rangle \,/\, \Delta f$  (V$^2$/Hz)',
                  fontsize=12)
    ax.set_title(r'Johnson Noise: $k_B$ Extraction via Slope Method',
                 fontsize=13)

    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    ax.set_xlim(5, 3e6)

    # Annotation box with result
    textstr = (f'$k_B$ = {k_B_measured:.4e} ± {sigma_kB:.1e} J/K\n'
               f'CODATA: {K_B_CODATA:.4e} J/K\n'
               f'Agreement: {pct_agree:.2f}%')
    props = dict(boxstyle='round', facecolor='white', alpha=0.85,
                 edgecolor='#cccccc')
    ax.text(0.97, 0.08, textstr, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom',
            horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig('plots/kB_extraction.png', dpi=200)
    plt.show()
    print("\n  Saved plots/kB_extraction.png")
