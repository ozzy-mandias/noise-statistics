import os, math

# ============================================================================
# FILE I/O
# ============================================================================

# Function load_trace: takes a single CSV file path from the GW-Instek GDS-1052-U oscilloscope.
# Reads the 16-line header and parses vertical scale (V/div) and sampling period (s).
# Converts the 4,000 raw ADC counts to volts using V = count * (vertical_scale / 25).
# Builds the time array using t[n] = n * sampling_period.
# Returns vertical scale, sampling period, voltage array, and time array.
def load_trace(file_name):
    file_object = open(file_name, "r")
    lines = file_object.readlines()

    vertical_scale  = float(lines[5].split(",")[1])
    sampling_period = float(lines[11].split(",")[1])

    voltages = []
    for line in lines[16:]:
        count = int(line.strip().rstrip(","))
        voltages.append(count * vertical_scale / 25)

    time = []
    for i in range(len(voltages)):
        time.append(i * sampling_period)

    file_object.close()
    return vertical_scale, sampling_period, voltages, time


# Function load_run: takes a directory path containing CSV files from the oscilloscope.
# Loops through each CSV file, calls load_trace on each one, and collects all voltage
# arrays into a list where each element is one trace (4,000 voltage samples).
# Returns the full collection of traces for the run.
def load_run(path):
    all_voltages = []
    for file in sorted(os.listdir(path)):
        if file.endswith(".CSV"):
            _, _, voltages, _ = load_trace(path + "/" + file)
            all_voltages.append(voltages)
    return all_voltages


# ============================================================================
# STATISTICAL MOMENT FUNCTIONS
# ============================================================================

def calc_average(run):
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += voltage
            count += 1
    return total / count


def calc_variance(run, average):
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += (voltage - average) ** 2
            count += 1
    return total / count


# Skewness and kurtosis are normalized by sigma^3 and sigma^4 respectively,
# so variance must be passed in to avoid recomputing it.
def calc_skewness(run, average, variance):
    sigma_cubed = variance ** 1.5
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += (voltage - average) ** 3
            count += 1
    return (total / count) / sigma_cubed


def calc_kurtosis(run, average, variance):
    sigma_to_the_fourth = variance ** 2
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += (voltage - average) ** 4
            count += 1
    return (total / count) / sigma_to_the_fourth


# ============================================================================
# ERROR ANALYSIS
# ============================================================================

# Standard deviation across 3 runs using Bessel correction (N-1 = 2).
def calc_std_dev(v1, v2, v3):
    average = (v1 + v2 + v3) / 3
    std_dev = math.sqrt(((v1 - average)**2 + (v2 - average)**2 + (v3 - average)**2) / 2)
    return std_dev


# ============================================================================
# DATA IMPORTS
# ============================================================================

# Amplifier baseline, gain 300, R_in = 1 Ohm
run1 = load_run("data/amp_noise/gain_300/LOG_1_OHM_run_1_gain_300_297.0K")
run2 = load_run("data/amp_noise/gain_300/LOG_1_OHM_run_2_gain_300_297.1K")
run3 = load_run("data/amp_noise/gain_300/LOG_1_OHM_run_3_gain_300_297.2K")

# Amplifier baseline, gain 200, R_in = 1 Ohm
# Required separately -- baseline variance scales with gain^2 so gain 300
# baseline cannot be reused for gain 200 measurements.
run4 = load_run("data/amp_noise/gain_200/LOG_1_OHM_run_1_gain_200_297.3K")
run5 = load_run("data/amp_noise/gain_200/LOG_1_OHM_run_2_gain_200_297.4K")
run6 = load_run("data/amp_noise/gain_200/LOG_1_OHM_run_3_gain_200_297.4K")

# Johnson noise, 1 MΩ, gain 200
# 1 MΩ required gain 200 to avoid clipping at 2V/div on the oscilloscope.
run7 = load_run("data/johnson_noise/1M_ohm/LOG_1_MOHM_run_1_gain_200_297.5K")
run8 = load_run("data/johnson_noise/1M_ohm/LOG_1_MOHM_run_2_gain_200_297.5K")
run9 = load_run("data/johnson_noise/1M_ohm/LOG_1_MOHM_run_3_gain_200_297.6K")

# Runs still to be collected (other resistor values):
# run_10ohm_a  = load_run("data/johnson_noise/10_ohms/...")
# run_100ohm_a = load_run("data/johnson_noise/100_ohms/...")
# run_1k_a     = load_run("data/johnson_noise/1k_ohms/...")
# run_10k_a    = load_run("data/johnson_noise/10k_ohms/...")
# run_100k_a   = load_run("data/johnson_noise/100k_ohms/...")


# ============================================================================
# AMPLIFIER BASELINE (gain 300)
# ============================================================================

run1_avg  = calc_average(run1)
run2_avg  = calc_average(run2)
run3_avg  = calc_average(run3)
run1_var  = calc_variance(run1, run1_avg)
run2_var  = calc_variance(run2, run2_avg)
run3_var  = calc_variance(run3, run3_avg)
run1_skew = calc_skewness(run1, run1_avg, run1_var)
run2_skew = calc_skewness(run2, run2_avg, run2_var)
run3_skew = calc_skewness(run3, run3_avg, run3_var)
run1_kurt = calc_kurtosis(run1, run1_avg, run1_var)
run2_kurt = calc_kurtosis(run2, run2_avg, run2_var)
run3_kurt = calc_kurtosis(run3, run3_avg, run3_var)

amp_baseline_300     = (run1_var  + run2_var  + run3_var)  / 3
amp_std_300          = calc_std_dev(run1_var, run2_var, run3_var)
amp_skew_300         = (run1_skew + run2_skew + run3_skew) / 3
amp_skew_std_300     = calc_std_dev(run1_skew, run2_skew, run3_skew)
amp_kurt_300         = (run1_kurt + run2_kurt + run3_kurt) / 3
amp_kurt_std_300     = calc_std_dev(run1_kurt, run2_kurt, run3_kurt)


# ============================================================================
# AMPLIFIER BASELINE (gain 200)
# ============================================================================

run4_avg  = calc_average(run4)
run5_avg  = calc_average(run5)
run6_avg  = calc_average(run6)
run4_var  = calc_variance(run4, run4_avg)
run5_var  = calc_variance(run5, run5_avg)
run6_var  = calc_variance(run6, run6_avg)
run4_skew = calc_skewness(run4, run4_avg, run4_var)
run5_skew = calc_skewness(run5, run5_avg, run5_var)
run6_skew = calc_skewness(run6, run6_avg, run6_var)
run4_kurt = calc_kurtosis(run4, run4_avg, run4_var)
run5_kurt = calc_kurtosis(run5, run5_avg, run5_var)
run6_kurt = calc_kurtosis(run6, run6_avg, run6_var)

amp_baseline_200     = (run4_var  + run5_var  + run6_var)  / 3
amp_std_200          = calc_std_dev(run4_var, run5_var, run6_var)
amp_skew_200         = (run4_skew + run5_skew + run6_skew) / 3
amp_skew_std_200     = calc_std_dev(run4_skew, run5_skew, run6_skew)
amp_kurt_200         = (run4_kurt + run5_kurt + run6_kurt) / 3
amp_kurt_std_200     = calc_std_dev(run4_kurt, run5_kurt, run6_kurt)


# ============================================================================
# JOHNSON NOISE (1 MΩ, gain 200)
# ============================================================================

run7_avg  = calc_average(run7)
run8_avg  = calc_average(run8)
run9_avg  = calc_average(run9)
run7_var  = calc_variance(run7, run7_avg)
run8_var  = calc_variance(run8, run8_avg)
run9_var  = calc_variance(run9, run9_avg)
run7_skew = calc_skewness(run7, run7_avg, run7_var)
run8_skew = calc_skewness(run8, run8_avg, run8_var)
run9_skew = calc_skewness(run9, run9_avg, run9_var)
run7_kurt = calc_kurtosis(run7, run7_avg, run7_var)
run8_kurt = calc_kurtosis(run8, run8_avg, run8_var)
run9_kurt = calc_kurtosis(run9, run9_avg, run9_var)

one_M_mean_var   = (run7_var  + run8_var  + run9_var)  / 3
one_M_std        = calc_std_dev(run7_var, run8_var, run9_var)
one_M_corrected  = one_M_mean_var - amp_baseline_200   # subtract gain 200 baseline
one_M_skew       = (run7_skew + run8_skew + run9_skew) / 3
one_M_skew_std   = calc_std_dev(run7_skew, run8_skew, run9_skew)
one_M_kurt       = (run7_kurt + run8_kurt + run9_kurt) / 3
one_M_kurt_std   = calc_std_dev(run7_kurt, run8_kurt, run9_kurt)

results = []
results.append((1000000, one_M_corrected, one_M_std, one_M_mean_var,
                one_M_skew, one_M_skew_std, one_M_kurt, one_M_kurt_std))


# ============================================================================
# PRINT STATEMENTS (GUARDED)
# ============================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AMPLIFIER NOISE BASELINE (gain 300, R_in = 1 Ohm)")
    print("=" * 60)
    print("  Run 1: var =", run1_var, " skew =", run1_skew, " kurt =", run1_kurt)
    print("  Run 2: var =", run2_var, " skew =", run2_skew, " kurt =", run2_kurt)
    print("  Run 3: var =", run3_var, " skew =", run3_skew, " kurt =", run3_kurt)
    print("  Baseline variance:", amp_baseline_300, "+/-", amp_std_300, "V^2")
    print("  Skewness:", amp_skew_300, "+/-", amp_skew_std_300, "(expect 0)")
    print("  Kurtosis:", amp_kurt_300, "+/-", amp_kurt_std_300, "(expect 3)")

    print("\n" + "=" * 60)
    print("AMPLIFIER NOISE BASELINE (gain 200, R_in = 1 Ohm)")
    print("=" * 60)
    print("  Run 4: var =", run4_var, " skew =", run4_skew, " kurt =", run4_kurt)
    print("  Run 5: var =", run5_var, " skew =", run5_skew, " kurt =", run5_kurt)
    print("  Run 6: var =", run6_var, " skew =", run6_skew, " kurt =", run6_kurt)
    print("  Baseline variance:", amp_baseline_200, "+/-", amp_std_200, "V^2")
    print("  Skewness:", amp_skew_200, "+/-", amp_skew_std_200, "(expect 0)")
    print("  Kurtosis:", amp_kurt_200, "+/-", amp_kurt_std_200, "(expect 3)")

    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 1M Ohm, gain 200)")
    print("=" * 60)
    print("  Run 7: var =", run7_var, " skew =", run7_skew, " kurt =", run7_kurt)
    print("  Run 8: var =", run8_var, " skew =", run8_skew, " kurt =", run8_kurt)
    print("  Run 9: var =", run9_var, " skew =", run9_skew, " kurt =", run9_kurt)
    print("  Mean variance:", one_M_mean_var, "+/-", one_M_std, "V^2")
    print("  Corrected (baseline subtracted):", one_M_corrected, "V^2")
    print("  Skewness:", one_M_skew, "+/-", one_M_skew_std, "(expect 0)")
    print("  Kurtosis:", one_M_kurt, "+/-", one_M_kurt_std, "(expect 3)")