# plot_histograms.py
#
# Plots voltage distribution histograms with Gaussian overlay for each
# measured resistor value. Visually confirms Gaussianity of Johnson noise.
# Imports raw run data and moment results from calc_moments.py.
#
# Currently active: amplifier baseline (gain 300, gain 200) and 1 MΩ.
# Other resistor values commented out pending data collection.

import numpy as np
import matplotlib.pyplot as plt
from calc_moments import (
    run1, run2, run3,
    run4, run5, run6,
    run7, run8, run9,
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
    ("Amp baseline (gain 300)", flatten([run1, run2, run3])),
    ("Amp baseline (gain 200)", flatten([run4, run5, run6])),
    ("1 MΩ (gain 200)",         flatten([run7, run8, run9])),
    # Pending data collection:
    # ("10 Ω",   flatten([run_10ohm_a,  run_10ohm_b,  run_10ohm_c ])),
    # ("100 Ω",  flatten([run_100ohm_a, run_100ohm_b, run_100ohm_c])),
    # ("1 kΩ",   flatten([run_1k_a,     run_1k_b,     run_1k_c    ])),
    # ("10 kΩ",  flatten([run_10k_a,    run_10k_b,    run_10k_c   ])),
    # ("100 kΩ", flatten([run_100k_a,   run_100k_b,   run_100k_c  ])),
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