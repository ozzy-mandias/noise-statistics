# plot_histograms.py
#
# Plots voltage distribution histograms with Gaussian overlay for each
# resistor value. Visually confirms Gaussianity of Johnson noise.
# Imports raw run data and moment results from calc_moments.py.

import numpy as np
import matplotlib.pyplot as plt
from calc_moments import (
    run3, run4, run5,
    run6, run7, run8,
    run9, run10, run11,
    run12, run13, run14,
    run15, run16, run17,
    run18, run19, run20,
    run21, run22, run23,
    results
)

def flatten(runs):  # takes a nested data structure - runs containing traces containing voltages, three levels deep - and collapses it into a single flat 1D array
    voltages = []
    for run in runs:
        for trace in run:
            for v in trace:
                voltages.append(v)
    return np.array(voltages)

datasets = [
    (10,      flatten([run3,  run4,  run5 ]),  "10 Ω"),
    (100,     flatten([run6,  run7,  run8 ]),  "100 Ω"),
    (1000,    flatten([run9,  run10, run11]),  "1 kΩ"),
    (10000,   flatten([run12, run13, run14]),  "10 kΩ (a)"),
    (10000,   flatten([run15, run16, run17]),  "10 kΩ (b)"),
    (100000,  flatten([run18, run19, run20]),  "100 kΩ"),
    (1000000, flatten([run21, run22, run23]),  "1 MΩ"),
]

fig, axes = plt.subplots(4, 2, figsize=(12, 16))
axes = axes.flatten()

for i, (R, voltages, label) in enumerate(datasets):
    ax = axes[i]
    mu = voltages.mean()
    sigma = voltages.std()

    ax.hist(voltages, bins=100, density=True, alpha=0.6, label='Data')

    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
    gaussian = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)  # Probability density function of a normal distribution
    ax.plot(x, gaussian, 'r-', linewidth=2, label='Gaussian fit')

    ax.set_title(label)
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Probability Density')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

axes[-1].set_visible(False) # hide empty 8th subplot

plt.suptitle('Voltage Distributions with Gaussian Overlay', fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig('plots/histograms.png', dpi=150)
plt.show()