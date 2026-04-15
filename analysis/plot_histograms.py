# plot_histograms.py
#
# Plots voltage distribution histograms with Gaussian overlay for each
# measured resistor value. Visually confirms Gaussianity of Johnson noise.
# Imports raw run data and moment results from calc_moments.py.
#
# Currently active: 10 Ω, 100 Ω, 1 kΩ, 10 kΩ, 1 MΩ.
# 100 kΩ pending data collection.

import numpy as np
import matplotlib.pyplot as plt
from calc_moments import (
    run7, run8, run9,
    run10, run11, run12,
    run13, run14, run15,
    run16, run17, run18,
    run19, run20, run21,
    results
)


def flatten(runs):
    # Collapses nested run -> trace -> voltage structure into a flat 1D array
    voltages = []
    for run in runs:
        for trace in run:
            for v in trace:
                voltages.append(v)
    return np.array(voltages)


datasets = [
    ("10 Ω (gain 300)",         flatten([run10, run11, run12])),
    ("100 Ω (gain 300)",        flatten([run13, run14, run15])),
    ("1 kΩ (gain 300)",         flatten([run16, run17, run18])),
    ("10 kΩ (gain 300)",        flatten([run19, run20, run21])),
    ("1 MΩ (gain 200)",         flatten([run7, run8, run9])),
]

n = len(datasets)
fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))
if n == 1:
    axes = [axes]

for ax, (label, voltages) in zip(axes, datasets):
    mu    = voltages.mean()
    sigma = voltages.std()

    ax.hist(voltages, bins=100, density=True, alpha=0.6, label="Data")

    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
    gaussian = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    ax.plot(x, gaussian, "r-", linewidth=2, label="Gaussian fit")

    ax.set_title(label)
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Probability Density")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

plt.suptitle("Voltage Distributions with Gaussian Overlay", fontsize=14)
plt.tight_layout()
plt.savefig("plots/histograms.png", dpi=150)
plt.show()