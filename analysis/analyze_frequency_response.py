# analyze_frequency_response.py
#
# AI DISCLAIMER: An AI tool (LLM) was used to assist in generating this
# comment for readability. The experimental methodology, analysis design,
# and code implementation are the author's own work.
#
# Characterizes the frequency response of the LLE preamp → HLE bandpass
# amplifier → SR1 chain, and computes the Noise Equivalent Bandwidth (NEBW)
# for use as Δf in the Johnson noise formula: ⟨V²⟩ = 4·k_B·T·R·Δf
#
# Input:  SR1 transfer function CSV from ./data/frequency_response/
#         Expected columns: frequency (Hz), magnitude (dB or linear)
#         Screenshot stored in same directory as lab notebook reference.
#
# Procedure:
#   1. Load transfer function CSV and parse frequency, |H(f)| columns
#   2. Convert to linear power: |H(f)|² (normalize so passband peak = 1)
#   3. Identify -3dB rolloff frequencies (f_low, f_high) for quick Δf estimate
#   4. Integrate |H(f)|² numerically (scipy.integrate.trapezoid) → Δf_NEB
#   5. Plot |H(f)|² vs frequency with -3dB points marked
#
# NEBW vs -3dB bandwidth:
#   The -3dB bandwidth (f_high - f_low) is an approximation. NEBW from the
#   numerical integral of |H(f)|² is the physically correct quantity to use
#   in the Johnson noise formula, accounting for soft rolloffs in the real
#   filter chain. Both are reported for comparison.
#
# Outputs: Δf_NEB (Hz), f_low (Hz), f_high (Hz), frequency response plot
#
# Downstream consumers:
#   extract_kB.py   — Δf_NEB used as Δf in ⟨V²⟩ = 4·k_B·T·R·Δf