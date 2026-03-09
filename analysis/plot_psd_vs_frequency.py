# plot_psd_vs_freq.py
#
#  Plots mean PSD (V²/Hz) vs frequency for all resistor values on a single
# axes with log-log scaling. Error bands show run-to-run std. Imports
# spectra list from calc_spectra.py.

# IN PROGRESS - NEED analyze_frequency_response.py FIRST TO NORMALIZE

import numpy as np
import matplotlib.pyplot as plt
from calc_spectra import spectra

fig, ax = plt.subplots(figsize=(10, 6))

labels = {
    10:      "10 Ω",
    100:     "100 Ω",
    1000:    "1 kΩ",
    10000:   "10 kΩ (a)",
    100000:  "100 kΩ",
    1000000: "1 MΩ",
}

seen = set()
for R, freq, mean_psd, std_psd, mean_vsd, std_vsd in spectra:
    if R == 10000 and R in seen:
        label = "10 kΩ (b)"
    else:
        label = labels.get(R, str(R) + " Ω")
    seen.add(R)

    ax.loglog(freq[1:], mean_psd[1:], label=label)
    ax.fill_between(freq[1:],
                    mean_psd[1:] - std_psd[1:],
                    mean_psd[1:] + std_psd[1:],
                    alpha=0.2)

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("PSD (V²/Hz)")
ax.set_title("Power Spectral Density vs Frequency")
ax.legend()
ax.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plots/psd_vs_freq.png", dpi=150)
plt.show()