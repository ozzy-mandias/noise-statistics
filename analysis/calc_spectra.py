# calc_spectra.py
#
# Computes Power Spectral Density (PSD, V²/Hz) and Voltage Spectral Density
# (VSD, V/√Hz) from raw oscilloscope voltage traces.
#
# Loader logic lives in calc_moments.py. load_trace() and load_run() are
# imported directly -- CSV parsing is not duplicated here.
#
# Spectral estimation uses Welch's method (scipy.signal.welch). The raw
# sample rate is 25 MHz (4e-8 s period), far above the 10 kHz passband.
# All traces in a run are concatenated, then decimated by 50 to give
# fs_eff = 500 kHz before Welch estimation. This keeps the frequency axis
# in the passband range while giving enough samples for stable estimates.
#
# One PSD is computed per run (three runs per resistor), then averaged.
#
# Inputs:  voltage arrays from load_run() in calc_moments.py; sampling_period
#          from load_trace()
# Outputs: spectra list of (R, freq, mean_psd, std_psd, mean_vsd, std_vsd)
#
# Downstream consumers:
#   plot_psd_vs_freq.py   -- flatness verification (whiteness)
#   plot_vsd_vs_R.py      -- slope extraction -> k_B
#   extract_kB.py         -- final Boltzmann constant determination

import numpy as np
from scipy.signal import welch, decimate
from calc_moments import load_run, load_trace

# ---------------------------------------------------------------------------
# Sample rate -- confirmed same across all runs
# ---------------------------------------------------------------------------
_, sampling_period, _, _ = load_trace("data/johnson_noise/10_ohms/LOG_10_OHM_run_1_gain_300_294.1K/DS0000.CSV")
fs = 1 / sampling_period   # 25 MHz

# Decimate to bring fs down to a range where Welch bins land in the passband.
# Factor of 50 gives fs_eff = 500 kHz; Nyquist = 250 kHz, well above 10 kHz.
# 476000 samples / 50 = 9520 samples per run -- enough for stable Welch estimates.
DECIMATION_FACTOR = 50
fs_eff = fs / DECIMATION_FACTOR

# ---------------------------------------------------------------------------
# Resistor runs
# (R, [path_run_a, path_run_b, path_run_c])
# ---------------------------------------------------------------------------
resistors = [
    (10,      ["data/johnson_noise/10_ohms/LOG_10_OHM_run_1_gain_300_294.1K",
               "data/johnson_noise/10_ohms/LOG_10_OHM_run_2_gain_300_294.1K",
               "data/johnson_noise/10_ohms/LOG_10_OHM_run_3_gain_300_294.2K"]),
    (100,     ["data/johnson_noise/100_ohms/LOG_100_OHM_run_1_gain_300_294.6K",
               "data/johnson_noise/100_ohms/LOG_100_OHM_run_2_gain_300_294.6K",
               "data/johnson_noise/100_ohms/LOG_100_OHM_run_3_gain_300_294.6K"]),
    (1000,    ["data/johnson_noise/1k_ohms/LOG_1_kOHM_run_1_gain_300_294.7K",
               "data/johnson_noise/1k_ohms/LOG_1_kOHM_run_2_gain_300_294.7K",
               "data/johnson_noise/1k_ohms/LOG_1_kOHM_run_3_gain_300_294.8K"]),
    (10000,   ["data/johnson_noise/10k_ohms/LOG_10_kOHM_run_1_gain_300_294.8K",
               "data/johnson_noise/10k_ohms/LOG_10_kOHM_run_2_gain_300_294.6K",
               "data/johnson_noise/10k_ohms/LOG_10_kOHM_run_3_gain_300_294.7K"]),
    (1000000, ["data/johnson_noise/1M_ohm/LOG_1_MOHM_run_1_gain_200_297.5K",
               "data/johnson_noise/1M_ohm/LOG_1_MOHM_run_2_gain_200_297.5K",
               "data/johnson_noise/1M_ohm/LOG_1_MOHM_run_3_gain_200_297.6K"]),
    # 100 kΩ pending data collection
]

spectra = []

for R, paths in resistors:
    psds = []
    for path in paths:
        # Concatenate all traces in this run into one array before decimating.
        # Decimating per-trace would leave too few samples for Welch.
        all_voltages = load_run(path)
        voltages_flat = []
        for trace in all_voltages:
            voltages_flat.extend(trace)
        voltages_np = np.array(voltages_flat)

        # Decimate then estimate PSD via Welch
        voltages_decimated = decimate(voltages_np, DECIMATION_FACTOR, ftype='fir')
        freq, psd = welch(voltages_decimated, fs=fs_eff, window='hann', nperseg=1024)
        psds.append(psd)

    psds     = np.array(psds)
    mean_psd = psds.mean(axis=0)
    std_psd  = psds.std(axis=0, ddof=1)
    mean_vsd = np.sqrt(mean_psd)
    # Error propagation: sigma_vsd = sigma_psd / (2 * sqrt(psd))
    std_vsd  = std_psd / (2 * mean_vsd)

    spectra.append((R, freq, mean_psd, std_psd, mean_vsd, std_vsd))