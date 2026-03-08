# calc_spectra.py
#
# AI DISCLAIMER: An AI tool (LLM) was used to assist in generating this
# comment for readability. The experimental methodology, analysis design,
# and code implementation are the author's own work.
#
# Computes Power Spectral Density (PSD, V²/Hz) and Voltage Spectral Density
# (VSD, V/√Hz) from raw oscilloscope voltage traces.
#
# Loader logic lives in calc_moments.py. load_trace() and load_run() are
# imported directly — CSV parsing is not duplicated here. Voltage arrays
# (Python lists) are converted to numpy arrays internally before processing.
#
# Spectral estimation uses Welch's method (scipy.signal.welch), which reduces
# PSD variance by averaging overlapping windowed periodograms. Sample rate is
# derived from the sampling_period metadata returned by load_trace().
#
# Inputs:  voltage arrays from load_run() in calc_moments.py; sampling_period
#          from load_trace()
# Outputs: freq (Hz), psd (V²/Hz), vsd (V/√Hz) arrays per resistor
#
# Downstream consumers:
#   plot_psd_vs_freq.py   — flatness verification (whiteness)
#   plot_vsd_vs_R.py      — slope extraction → k_B
#   extract_kB.py         — final Boltzmann constant determination

