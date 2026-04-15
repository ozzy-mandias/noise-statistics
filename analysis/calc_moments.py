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

# Johnson noise, 10 Ohm, gain 300
run10 = load_run("data/johnson_noise/10_ohms/LOG_10_OHM_run_1_gain_300_294.1K")
run11 = load_run("data/johnson_noise/10_ohms/LOG_10_OHM_run_2_gain_300_294.1K")
run12 = load_run("data/johnson_noise/10_ohms/LOG_10_OHM_run_3_gain_300_294.2K")

# Johnson noise, 100 Ohm, gain 300
run13 = load_run("data/johnson_noise/100_ohms/LOG_100_OHM_run_1_gain_300_294.6K")
run14 = load_run("data/johnson_noise/100_ohms/LOG_100_OHM_run_2_gain_300_294.6K")
run15 = load_run("data/johnson_noise/100_ohms/LOG_100_OHM_run_3_gain_300_294.6K")

# Johnson noise, 1 kOhm, gain 300
run16 = load_run("data/johnson_noise/1k_ohms/LOG_1_kOHM_run_1_gain_300_294.7K")
run17 = load_run("data/johnson_noise/1k_ohms/LOG_1_kOHM_run_2_gain_300_294.7K")
run18 = load_run("data/johnson_noise/1k_ohms/LOG_1_kOHM_run_3_gain_300_294.8K")

# Johnson noise, 10 kOhm, gain 300
run19 = load_run("data/johnson_noise/10k_ohms/LOG_10_kOHM_run_1_gain_300_294.8K")
run20 = load_run("data/johnson_noise/10k_ohms/LOG_10_kOHM_run_2_gain_300_294.6K")
run21 = load_run("data/johnson_noise/10k_ohms/LOG_10_kOHM_run_3_gain_300_294.7K")

# 100 kOhm data still to be collected:
# run_100k_a = load_run("data/johnson_noise/100k_ohms/...")


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

# ============================================================================
# JOHNSON NOISE (10 Ohm, gain 300)
# ============================================================================

run10_avg  = calc_average(run10)
run11_avg  = calc_average(run11)
run12_avg  = calc_average(run12)
run10_var  = calc_variance(run10, run10_avg)
run11_var  = calc_variance(run11, run11_avg)
run12_var  = calc_variance(run12, run12_avg)
run10_skew = calc_skewness(run10, run10_avg, run10_var)
run11_skew = calc_skewness(run11, run11_avg, run11_var)
run12_skew = calc_skewness(run12, run12_avg, run12_var)
run10_kurt = calc_kurtosis(run10, run10_avg, run10_var)
run11_kurt = calc_kurtosis(run11, run11_avg, run11_var)
run12_kurt = calc_kurtosis(run12, run12_avg, run12_var)

ten_ohm_mean_var  = (run10_var  + run11_var  + run12_var)  / 3
ten_ohm_std       = calc_std_dev(run10_var, run11_var, run12_var)
ten_ohm_corrected = ten_ohm_mean_var - amp_baseline_300
ten_ohm_skew      = (run10_skew + run11_skew + run12_skew) / 3
ten_ohm_skew_std  = calc_std_dev(run10_skew, run11_skew, run12_skew)
ten_ohm_kurt      = (run10_kurt + run11_kurt + run12_kurt) / 3
ten_ohm_kurt_std  = calc_std_dev(run10_kurt, run11_kurt, run12_kurt)


# ============================================================================
# JOHNSON NOISE (100 Ohm, gain 300)
# ============================================================================

run13_avg  = calc_average(run13)
run14_avg  = calc_average(run14)
run15_avg  = calc_average(run15)
run13_var  = calc_variance(run13, run13_avg)
run14_var  = calc_variance(run14, run14_avg)
run15_var  = calc_variance(run15, run15_avg)
run13_skew = calc_skewness(run13, run13_avg, run13_var)
run14_skew = calc_skewness(run14, run14_avg, run14_var)
run15_skew = calc_skewness(run15, run15_avg, run15_var)
run13_kurt = calc_kurtosis(run13, run13_avg, run13_var)
run14_kurt = calc_kurtosis(run14, run14_avg, run14_var)
run15_kurt = calc_kurtosis(run15, run15_avg, run15_var)

hundred_ohm_mean_var  = (run13_var  + run14_var  + run15_var)  / 3
hundred_ohm_std       = calc_std_dev(run13_var, run14_var, run15_var)
hundred_ohm_corrected = hundred_ohm_mean_var - amp_baseline_300
hundred_ohm_skew      = (run13_skew + run14_skew + run15_skew) / 3
hundred_ohm_skew_std  = calc_std_dev(run13_skew, run14_skew, run15_skew)
hundred_ohm_kurt      = (run13_kurt + run14_kurt + run15_kurt) / 3
hundred_ohm_kurt_std  = calc_std_dev(run13_kurt, run14_kurt, run15_kurt)


# ============================================================================
# JOHNSON NOISE (1 kOhm, gain 300)
# ============================================================================

run16_avg  = calc_average(run16)
run17_avg  = calc_average(run17)
run18_avg  = calc_average(run18)
run16_var  = calc_variance(run16, run16_avg)
run17_var  = calc_variance(run17, run17_avg)
run18_var  = calc_variance(run18, run18_avg)
run16_skew = calc_skewness(run16, run16_avg, run16_var)
run17_skew = calc_skewness(run17, run17_avg, run17_var)
run18_skew = calc_skewness(run18, run18_avg, run18_var)
run16_kurt = calc_kurtosis(run16, run16_avg, run16_var)
run17_kurt = calc_kurtosis(run17, run17_avg, run17_var)
run18_kurt = calc_kurtosis(run18, run18_avg, run18_var)

one_k_mean_var  = (run16_var  + run17_var  + run18_var)  / 3
one_k_std       = calc_std_dev(run16_var, run17_var, run18_var)
one_k_corrected = one_k_mean_var - amp_baseline_300
one_k_skew      = (run16_skew + run17_skew + run18_skew) / 3
one_k_skew_std  = calc_std_dev(run16_skew, run17_skew, run18_skew)
one_k_kurt      = (run16_kurt + run17_kurt + run18_kurt) / 3
one_k_kurt_std  = calc_std_dev(run16_kurt, run17_kurt, run18_kurt)


# ============================================================================
# JOHNSON NOISE (10 kOhm, gain 300)
# ============================================================================

run19_avg  = calc_average(run19)
run20_avg  = calc_average(run20)
run21_avg  = calc_average(run21)
run19_var  = calc_variance(run19, run19_avg)
run20_var  = calc_variance(run20, run20_avg)
run21_var  = calc_variance(run21, run21_avg)
run19_skew = calc_skewness(run19, run19_avg, run19_var)
run20_skew = calc_skewness(run20, run20_avg, run20_var)
run21_skew = calc_skewness(run21, run21_avg, run21_var)
run19_kurt = calc_kurtosis(run19, run19_avg, run19_var)
run20_kurt = calc_kurtosis(run20, run20_avg, run20_var)
run21_kurt = calc_kurtosis(run21, run21_avg, run21_var)

ten_k_mean_var  = (run19_var  + run20_var  + run21_var)  / 3
ten_k_std       = calc_std_dev(run19_var, run20_var, run21_var)
ten_k_corrected = ten_k_mean_var - amp_baseline_300
ten_k_skew      = (run19_skew + run20_skew + run21_skew) / 3
ten_k_skew_std  = calc_std_dev(run19_skew, run20_skew, run21_skew)
ten_k_kurt      = (run19_kurt + run20_kurt + run21_kurt) / 3
ten_k_kurt_std  = calc_std_dev(run19_kurt, run20_kurt, run21_kurt)


# ============================================================================
# RESULTS
# ============================================================================

results = []
results.append((10,      ten_ohm_corrected,     ten_ohm_std,     ten_ohm_mean_var,
                ten_ohm_skew,     ten_ohm_skew_std,     ten_ohm_kurt,     ten_ohm_kurt_std))
results.append((100,     hundred_ohm_corrected, hundred_ohm_std, hundred_ohm_mean_var,
                hundred_ohm_skew, hundred_ohm_skew_std, hundred_ohm_kurt, hundred_ohm_kurt_std))
results.append((1000,    one_k_corrected,       one_k_std,       one_k_mean_var,
                one_k_skew,       one_k_skew_std,       one_k_kurt,       one_k_kurt_std))
results.append((10000,   ten_k_corrected,       ten_k_std,       ten_k_mean_var,
                ten_k_skew,       ten_k_skew_std,       ten_k_kurt,       ten_k_kurt_std))
results.append((1000000, one_M_corrected,       one_M_std,       one_M_mean_var,
                one_M_skew,       one_M_skew_std,       one_M_kurt,       one_M_kurt_std))


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
    print("JOHNSON NOISE (R_in = 10 Ohm, gain 300)")
    print("=" * 60)
    print("  Run 10: var =", run10_var, " skew =", run10_skew, " kurt =", run10_kurt)
    print("  Run 11: var =", run11_var, " skew =", run11_skew, " kurt =", run11_kurt)
    print("  Run 12: var =", run12_var, " skew =", run12_skew, " kurt =", run12_kurt)
    print("  Mean variance:", ten_ohm_mean_var, "+/-", ten_ohm_std, "V^2")
    print("  Corrected (baseline subtracted):", ten_ohm_corrected, "V^2")
    print("  Skewness:", ten_ohm_skew, "+/-", ten_ohm_skew_std, "(expect 0)")
    print("  Kurtosis:", ten_ohm_kurt, "+/-", ten_ohm_kurt_std, "(expect 3)")

    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 100 Ohm, gain 300)")
    print("=" * 60)
    print("  Run 13: var =", run13_var, " skew =", run13_skew, " kurt =", run13_kurt)
    print("  Run 14: var =", run14_var, " skew =", run14_skew, " kurt =", run14_kurt)
    print("  Run 15: var =", run15_var, " skew =", run15_skew, " kurt =", run15_kurt)
    print("  Mean variance:", hundred_ohm_mean_var, "+/-", hundred_ohm_std, "V^2")
    print("  Corrected (baseline subtracted):", hundred_ohm_corrected, "V^2")
    print("  Skewness:", hundred_ohm_skew, "+/-", hundred_ohm_skew_std, "(expect 0)")
    print("  Kurtosis:", hundred_ohm_kurt, "+/-", hundred_ohm_kurt_std, "(expect 3)")

    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 1 kOhm, gain 300)")
    print("=" * 60)
    print("  Run 16: var =", run16_var, " skew =", run16_skew, " kurt =", run16_kurt)
    print("  Run 17: var =", run17_var, " skew =", run17_skew, " kurt =", run17_kurt)
    print("  Run 18: var =", run18_var, " skew =", run18_skew, " kurt =", run18_kurt)
    print("  Mean variance:", one_k_mean_var, "+/-", one_k_std, "V^2")
    print("  Corrected (baseline subtracted):", one_k_corrected, "V^2")
    print("  Skewness:", one_k_skew, "+/-", one_k_skew_std, "(expect 0)")
    print("  Kurtosis:", one_k_kurt, "+/-", one_k_kurt_std, "(expect 3)")

    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 10 kOhm, gain 300)")
    print("=" * 60)
    print("  Run 19: var =", run19_var, " skew =", run19_skew, " kurt =", run19_kurt)
    print("  Run 20: var =", run20_var, " skew =", run20_skew, " kurt =", run20_kurt)
    print("  Run 21: var =", run21_var, " skew =", run21_skew, " kurt =", run21_kurt)
    print("  Mean variance:", ten_k_mean_var, "+/-", ten_k_std, "V^2")
    print("  Corrected (baseline subtracted):", ten_k_corrected, "V^2")
    print("  Skewness:", ten_k_skew, "+/-", ten_k_skew_std, "(expect 0)")
    print("  Kurtosis:", ten_k_kurt, "+/-", ten_k_kurt_std, "(expect 3)")

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