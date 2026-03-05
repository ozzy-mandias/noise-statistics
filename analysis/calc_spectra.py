# calc_spectra.py
#
# AI DISCLAIMER: An AI tool (LLM) was used to assist in generating this
# comment for readability. The experimental methodology, analysis design,
# and code implementation are the author's own work.
#
# Computes Power Spectral Density (PSD, V²/Hz) and Voltage Spectral Density
# (VSD, V/√Hz) from raw oscilloscope CSV traces.
#
# Loader logic is intentionally omitted here. CSV parsing and array construction
# are handled by load_trace() and load_run() in calc_moments.py — import from
# there rather than duplicating. calc_spectra.py receives clean numpy arrays
# and is responsible only for spectral estimation.
#
# Spectral estimation uses Welch's method (scipy.signal.welch), which averages
# overlapping windowed periodograms to reduce variance on the PSD estimate.
# Sample rate is inferred from the time column of the oscilloscope CSV.
#
# Inputs:  raw voltage arrays from load_run() in calc_moments.py
# Outputs: freq (Hz), psd (V²/Hz), vsd (V/√Hz) arrays per resistor
#
# Downstream consumers:
#   plot_psd_vs_freq.py   — flatness verification (whiteness)
#   plot_vsd_vs_R.py      — slope extraction → k_B
#   extract_kB.py         — final Boltzmann constant determination