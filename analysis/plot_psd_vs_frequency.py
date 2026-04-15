# plot_psd_vs_freq.py
#
# Plots mean PSD (V²/Hz) vs frequency for all resistor values on a single
# axes with log-log scaling. Error bands show run-to-run std. Imports
# spectra list from calc_spectra.py.
#
# The PSD here is raw (not normalized by the amplifier transfer function).
# Normalization by |H(f)|^2 comes in extract_kB.py after NEBW is confirmed.
#
# Inputs:  spectra list from calc_spectra.py
# Outputs: plots/psd_vs_freq.png

import numpy as np
import matplotlib.pyplot as plt
from calc_spectra import spectra

fig, ax = plt.subplots(figsize=(10, 6))

labels = {
    10:      "10 Ω",
    100:     "100 Ω",
    1000:    "1 kΩ",
    10000:   "10 kΩ",
    1000000: "1 MΩ",
}

for R, freq, mean_psd, std_psd, mean_vsd, std_vsd in spectra:
    label = labels.get(R, str(R) + " Ω")

    # Skip DC bin (index 0) -- always zero or artifactual
    ax.loglog(freq[1:], mean_psd[1:], label=label)

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("PSD (V²/Hz)")
ax.set_title("Power Spectral Density vs Frequency")
ax.legend(loc='upper right')
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.set_xlim(freq[1], 250000)
ax.set_ylim(1e-7, 1e-3)
plt.tight_layout()
plt.savefig("plots/psd_vs_freq.png", dpi=150)
plt.show()