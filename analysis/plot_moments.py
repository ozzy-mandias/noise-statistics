# plot_moments.py
#
# Plots statistical moments (variance, skewness, kurtosis) vs resistor value.
# Imports results list from calc_moments.py.
#
# Active resistors: 10 Ω, 100 Ω, 1 kΩ, 10 kΩ, 1 MΩ.
# 100 kΩ pending data collection.

import numpy as np
import matplotlib.pyplot as plt
from calc_moments import results

R_vals    = [row[0] for row in results]
corr_vars = [row[1] for row in results]
var_errs  = [row[2] for row in results]
skews     = [row[4] for row in results]
skew_errs = [row[5] for row in results]
kurts     = [row[6] for row in results]
kurt_errs = [row[7] for row in results]

fig, axes = plt.subplots(3, 1, figsize=(8, 12))

# Variance vs R
axes[0].errorbar(R_vals, corr_vars, yerr=var_errs, fmt='o', capsize=4)
axes[0].set_xscale("log")
axes[0].set_yscale("log")
axes[0].set_xlabel("Resistance (Ω)")
axes[0].set_ylabel("Corrected Variance (V²)")
axes[0].set_title("Variance vs Resistance")
axes[0].grid(True, which="both", linestyle="--", alpha=0.5)

# Skewness vs R
axes[1].errorbar(R_vals, skews, yerr=skew_errs, fmt='o', capsize=4)
axes[1].axhline(0, color="red", linestyle="--", label="Expected: 0")
axes[1].set_xscale("log")
axes[1].set_xlabel("Resistance (Ω)")
axes[1].set_ylabel("Skewness")
axes[1].set_title("Skewness vs Resistance")
axes[1].legend()
axes[1].grid(True, linestyle="--", alpha=0.5)

# Kurtosis vs R
axes[2].errorbar(R_vals, kurts, yerr=kurt_errs, fmt='o', capsize=4)
axes[2].axhline(3, color="red", linestyle="--", label="Expected: 3")
axes[2].set_xscale("log")
axes[2].set_xlabel("Resistance (Ω)")
axes[2].set_ylabel("Kurtosis")
axes[2].set_title("Kurtosis vs Resistance")
axes[2].legend()
axes[2].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("plots/moments.png", dpi=150)
plt.show()