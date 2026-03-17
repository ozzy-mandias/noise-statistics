# analyze_frequency_response.py
#
# Plots the amplifier frequency response (dBrA vs Hz) for gain 200 and 300.
# Data is from SR1 ratio mode chirp sweeps exported as .TXT files.
# NEBW computation comes later, after verifying the curves look correct.

import numpy as np
import matplotlib.pyplot as plt

SWEEP_FILES = {
    200: "data/frequency_response/frequency_response_gain_200.TXT",
    300: "data/frequency_response/frequency_response_gain_300.TXT",
}

def parse_sr1_file(filepath):
    freqs, powers_db = [], []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("//") or line == "":
                continue
            parts = line.split(",")
            if len(parts) != 2:
                continue
            try:
                freq, db = float(parts[0]), float(parts[1])
            except ValueError:
                continue
            if freq == 0.0:
                continue
            freqs.append(freq)
            powers_db.append(db)
    return np.array(freqs), np.array(powers_db)

fig, ax = plt.subplots(figsize=(10, 6))

for gain, filepath in SWEEP_FILES.items():
    freq, db = parse_sr1_file(filepath)
    ax.semilogx(freq, db, label=f"Gain {gain}")

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("|H(f)|²  (dBrA)")
ax.set_title("Amplifier Frequency Response -- SR1 Ratio Mode")
ax.legend()
ax.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plots/frequency_response.png", dpi=150)
plt.show()