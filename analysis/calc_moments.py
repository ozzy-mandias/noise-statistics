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
    file_object = open(file_name, "r")                  # Open file
    lines = file_object.readlines()                     # Return each line in the csv as a stringl store in variable, lines
    # print(lines[16:])                                 # For debugging; skips metadata (first 16 lines)

    vertical_scale = float(lines[5].split(",")[1])      # Parse metadata, convert string to float to store vertical scale
    sampling_period = float(lines[11].split(",")[1])    # ^ Same, but for sampling period metadata

    voltages = []                                       # Loop to convert each line to an integer, multiply by vertical_scale /25 to put it into volts
    for line in lines[16:]:
        count = int(line.strip().rstrip(","))           # .strip() removes the newline, then .rstrip(",") removes the trailing comma
        voltages.append(count * vertical_scale / 25)

    time = []                                           # Building the time array the same way
    for i in range(len(voltages)):
        time.append(i * sampling_period)

    file_object.close()                                 # Close file

    return vertical_scale, sampling_period, voltages, time

# Function load_run: takes a directory path containing LOG folders from the oscilloscope.
# Loops through each LOG folder, finds all CSV files inside, and calls load_trace on each one.
# Collects all voltage arrays into a list where each element is one trace (4,000 voltage samples).
# Returns the full collection of traces across all runs.

def load_run(path):
    all_voltages = []
    for file in os.listdir(path):
        if file.endswith(".CSV"):
            vert_scale, samp_period, voltages, time = load_trace(path + "/" + file)
            all_voltages.append(voltages)
    return all_voltages

# ============================================================================
# DATA IMPORTS
# ============================================================================

# Storing amplifier noise data from ./data/amp_noise into variables that can be accessed here (3 runs of the same measurement)
run1 = load_run("data/amp_noise/gain_300/LOG0001")
run0 = load_run("data/amp_noise/gain_300/LOG0000")  
run2 = load_run("data/amp_noise/gain_300/LOG0002")

# Storing Johnson noise data for a 10 Ohm resistor from ./data/johnson_noise ... (3 runs of the same measurement)
run3 = load_run("data/johnson_noise/10_ohms/LOG0003")
run4 = load_run("data/johnson_noise/10_ohms/LOG0004")
run5 = load_run("data/johnson_noise/10_ohms/LOG0005")

# Storing Johnson noise data for a 100 Ohm resistor
run6 = load_run("data/johnson_noise/100_ohms/LOG0006")
run7 = load_run("data/johnson_noise/100_ohms/LOG0007")
run8 = load_run("data/johnson_noise/100_ohms/LOG0008")

# Storing Johnson noise data for a 1k Ohm resistor
run9 = load_run("data/johnson_noise/1k_ohms/LOG0009")
run10 = load_run("data/johnson_noise/1k_ohms/LOG0010")
run11 = load_run("data/johnson_noise/1k_ohms/LOG0011")

# Storing Johnson noise data for a 10k Ohm resistor
run12 = load_run("data/johnson_noise/10k_ohms/LOG0012")
run13 = load_run("data/johnson_noise/10k_ohms/LOG0013")
run14 = load_run("data/johnson_noise/10k_ohms/LOG0014")

# Storing Johnson noise data for a 10k Ohm resistor* NOTE! Repeated accidentally
run15 = load_run("data/johnson_noise/10k_ohms/LOG0015")
run16 = load_run("data/johnson_noise/10k_ohms/LOG0016")
run17 = load_run("data/johnson_noise/10k_ohms/LOG0017")

# Storing Johnson noise data for a 100k Ohm resistor
run18 = load_run("data/johnson_noise/100k_ohms/LOG0018")
run19 = load_run("data/johnson_noise/100k_ohms/LOG0019")
run20 = load_run("data/johnson_noise/100k_ohms/LOG0020")

# Johnson noise from the 1M Ohm resistor was clipping on the scope when its verticial scale was 2V/div,
# which truncates the tails of the Gaussian distribution- corrupting variance, skewness, and kurtosis 
# measurements since those are sensitive to the tails. At 5V/div the ADC resolution drops, increasing
# quantization noise floor relative to your signal.

# This is an instrument tradeoff, so I opted to to lower the gain in the HLE from 300x to 200x. This required
# me to a quantify a new amplifier noise baseline at those settings. The baseline variance scales with gain squared,
# so a different gain stage gives a different baseline that I can't derive from my existing 300-gain measurements.

# Storing amplifier noise data from ./data/amp_noise into variables that can be accessed here (3 runs of the same measurement)
run24 = load_run("data/amp_noise/gain_200/LOG0024")
run25 = load_run("data/amp_noise/gain_200/LOG0025")  
run26 = load_run("data/amp_noise/gain_200/LOG0026")

# Storing Johnson noise data for a 1M Ohm resistor
run21 = load_run("data/johnson_noise/1M_ohm/LOG0021")
run22 = load_run("data/johnson_noise/1M_ohm/LOG0022")
run23 = load_run("data/johnson_noise/1M_ohm/LOG0023")

# ============================================================================
# FUNCTIONS FOR CALCULATING STATISTICAL MOMENTS
# ============================================================================

# Average
def calc_average(run):                     
    total = 0
    count = 0

    for trace in run:
        for voltage in trace:
            total += voltage
            count += 1
    return total / count

# Variance
def calc_variance(run, average):            
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += (voltage - average) ** 2
            count += 1
    return total / count

# For skewness and kurtosis, variance needs to be passed to calculate sigma^3, for skewness, and sigma^4, for kurtosis, so that they can be normalized

# Skewness
def calc_skewness(run, average, variance):
    sigma_cubed = variance ** 1.5            
    total = 0
    count = 0
    for trace in run:
        for voltage in trace:
            total += (voltage - average) ** 3
            count += 1
    return (total / count) / sigma_cubed
    
# Kurtosis
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
# FUNCTION(S) FOR ERROR ANALYSIS
# ============================================================================

# Standard Deviation
def calc_std_dev(v1, v2, v3):       # v1 is the variance of the first run, and so forth...
    average = (v1 + v2 + v3) / 3
    std_dev = math.sqrt(((v1 - average)**2 + (v2 - average)**2 + (v3 - average)**2) / 2) # IMPORTANT! The / 2 is the N-1 Bessel correction since N=3.
    return std_dev

# ============================================================================
# AMPLIFIER NOISE
# ============================================================================

# Data storage: amplifier baseline (gain_300, R_in = 1 Ohm)
run0_avg = calc_average(run0)
run1_avg = calc_average(run1)
run2_avg = calc_average(run2)
run0_var = calc_variance(run0, run0_avg)
run1_var = calc_variance(run1, run1_avg)
run2_var = calc_variance(run2, run2_avg)
run0_skew = calc_skewness(run0, run0_avg, run0_var)
run1_skew = calc_skewness(run1, run1_avg, run1_var)
run2_skew = calc_skewness(run2, run2_avg, run2_var)
run0_kurt = calc_kurtosis(run0, run0_avg, run0_var)
run1_kurt = calc_kurtosis(run1, run1_avg, run1_var)
run2_kurt = calc_kurtosis(run2, run2_avg, run2_var)
amp_baseline = (run0_var + run1_var + run2_var) / 3
amp_std = calc_std_dev(run0_var, run1_var, run2_var)
amp_skew = (run0_skew + run1_skew + run2_skew) / 3
amp_skew_std = calc_std_dev(run0_skew, run1_skew, run2_skew)
amp_kurt = (run0_kurt + run1_kurt + run2_kurt) / 3
amp_kurt_std = calc_std_dev(run0_kurt, run1_kurt, run2_kurt)

# Data storage: amplifier baseline (gain_200, R_in = 1 Ohm)
run24_avg = calc_average(run24)
run25_avg = calc_average(run25)
run26_avg = calc_average(run26)
run24_var = calc_variance(run24, run24_avg)
run25_var = calc_variance(run25, run25_avg)
run26_var = calc_variance(run26, run26_avg)
run24_skew = calc_skewness(run24, run24_avg, run24_var)
run25_skew = calc_skewness(run25, run25_avg, run25_var)
run26_skew = calc_skewness(run26, run26_avg, run26_var)
run24_kurt = calc_kurtosis(run24, run24_avg, run24_var)
run25_kurt = calc_kurtosis(run25, run25_avg, run25_var)
run26_kurt = calc_kurtosis(run26, run26_avg, run26_var)
amp_baseline_200 = (run24_var + run25_var + run26_var) / 3
amp_std_200 = calc_std_dev(run24_var, run25_var, run26_var)
amp_skew_200 = (run24_skew + run25_skew + run26_skew) / 3
amp_skew_std_200 = calc_std_dev(run24_skew, run25_skew, run26_skew)
amp_kurt_200 = (run24_kurt + run25_kurt + run26_kurt) / 3
amp_kurt_std_200 = calc_std_dev(run24_kurt, run25_kurt, run26_kurt)

# ============================================================================
# JOHNSON NOISE
# ============================================================================
results = []

# OUTPUT: Johnson Noise (R_in = 10 Ohm)
run3_avg = calc_average(run3)
run4_avg = calc_average(run4)
run5_avg = calc_average(run5)
run3_var = calc_variance(run3, run3_avg)
run4_var = calc_variance(run4, run4_avg)
run5_var = calc_variance(run5, run5_avg)
run3_skew = calc_skewness(run3, run3_avg, run3_var)
run4_skew = calc_skewness(run4, run4_avg, run4_var)
run5_skew = calc_skewness(run5, run5_avg, run5_var)
run3_kurt = calc_kurtosis(run3, run3_avg, run3_var)
run4_kurt = calc_kurtosis(run4, run4_avg, run4_var)
run5_kurt = calc_kurtosis(run5, run5_avg, run5_var)
ten_ohm_mean_var = (run3_var + run4_var + run5_var) / 3
ten_ohm_std = calc_std_dev(run3_var, run4_var, run5_var)
ten_ohm_corrected = ten_ohm_mean_var - amp_baseline
ten_ohm_skew = (run3_skew + run4_skew + run5_skew) / 3
ten_ohm_skew_std = calc_std_dev(run3_skew, run4_skew, run5_skew)
ten_ohm_kurt = (run3_kurt + run4_kurt + run5_kurt) / 3
ten_ohm_kurt_std = calc_std_dev(run3_kurt, run4_kurt, run5_kurt)

results.append((10, ten_ohm_corrected, ten_ohm_std, ten_ohm_mean_var, ten_ohm_skew, ten_ohm_skew_std, ten_ohm_kurt, ten_ohm_kurt_std))

# Johnson Noise (R_in = 100 Ohm)
run6_avg = calc_average(run6)
run7_avg = calc_average(run7)
run8_avg = calc_average(run8)
run6_var = calc_variance(run6, run6_avg)
run7_var = calc_variance(run7, run7_avg)
run8_var = calc_variance(run8, run8_avg)
run6_skew = calc_skewness(run6, run6_avg, run6_var)
run7_skew = calc_skewness(run7, run7_avg, run7_var)
run8_skew = calc_skewness(run8, run8_avg, run8_var)
run6_kurt = calc_kurtosis(run6, run6_avg, run6_var)
run7_kurt = calc_kurtosis(run7, run7_avg, run7_var)
run8_kurt = calc_kurtosis(run8, run8_avg, run8_var)
hundred_ohm_mean_var = (run6_var + run7_var + run8_var) / 3
hundred_ohm_std = calc_std_dev(run6_var, run7_var, run8_var)
hundred_ohm_corrected = hundred_ohm_mean_var - amp_baseline
hundred_ohm_skew = (run6_skew + run7_skew + run8_skew) / 3
hundred_ohm_skew_std = calc_std_dev(run6_skew, run7_skew, run8_skew)
hundred_ohm_kurt = (run6_kurt + run7_kurt + run8_kurt) / 3
hundred_ohm_kurt_std = calc_std_dev(run6_kurt, run7_kurt, run8_kurt)

results.append((100, hundred_ohm_corrected, hundred_ohm_std, hundred_ohm_mean_var, hundred_ohm_skew, hundred_ohm_skew_std, hundred_ohm_kurt, hundred_ohm_kurt_std))

# Johnson Noise (R_in = 1k Ohm)
run9_avg = calc_average(run9)
run10_avg = calc_average(run10)
run11_avg = calc_average(run11)
run9_var = calc_variance(run9, run9_avg)
run10_var = calc_variance(run10, run10_avg)
run11_var = calc_variance(run11, run11_avg)
run9_skew = calc_skewness(run9, run9_avg, run9_var)
run10_skew = calc_skewness(run10, run10_avg, run10_var)
run11_skew = calc_skewness(run11, run11_avg, run11_var)
run9_kurt = calc_kurtosis(run9, run9_avg, run9_var)
run10_kurt = calc_kurtosis(run10, run10_avg, run10_var)
run11_kurt = calc_kurtosis(run11, run11_avg, run11_var)
one_k_mean_var = (run9_var + run10_var + run11_var) / 3
one_k_std = calc_std_dev(run9_var, run10_var, run11_var)
one_k_corrected = one_k_mean_var - amp_baseline
one_k_skew = (run9_skew + run10_skew + run11_skew) / 3
one_k_skew_std = calc_std_dev(run9_skew, run10_skew, run11_skew)
one_k_kurt = (run9_kurt + run10_kurt + run11_kurt) / 3
one_k_kurt_std = calc_std_dev(run9_kurt, run10_kurt, run11_kurt)

results.append((1000, one_k_corrected, one_k_std, one_k_mean_var, one_k_skew, one_k_skew_std, one_k_kurt, one_k_kurt_std))

# Johnson Noise (R_in = 10k Ohm)
run12_avg = calc_average(run12)
run13_avg = calc_average(run13)
run14_avg = calc_average(run14)
run12_var = calc_variance(run12, run12_avg)
run13_var = calc_variance(run13, run13_avg)
run14_var = calc_variance(run14, run14_avg)
run12_skew = calc_skewness(run12, run12_avg, run12_var)
run13_skew = calc_skewness(run13, run13_avg, run13_var)
run14_skew = calc_skewness(run14, run14_avg, run14_var)
run12_kurt = calc_kurtosis(run12, run12_avg, run12_var)
run13_kurt = calc_kurtosis(run13, run13_avg, run13_var)
run14_kurt = calc_kurtosis(run14, run14_avg, run14_var)
ten_k_mean_var = (run12_var + run13_var + run14_var) / 3
ten_k_std = calc_std_dev(run12_var, run13_var, run14_var)
ten_k_corrected = ten_k_mean_var - amp_baseline
ten_k_skew = (run12_skew + run13_skew + run14_skew) / 3
ten_k_skew_std = calc_std_dev(run12_skew, run13_skew, run14_skew)
ten_k_kurt = (run12_kurt + run13_kurt + run14_kurt) / 3
ten_k_kurt_std = calc_std_dev(run12_kurt, run13_kurt, run14_kurt)

results.append((10000, ten_k_corrected, ten_k_std, ten_k_mean_var, ten_k_skew, ten_k_skew_std, ten_k_kurt, ten_k_kurt_std))

# Johnson Noise (R_in = 10k Ohm)* NOTE! Repeated accidentally, denoted as run "b"
run15_avg = calc_average(run15)
run16_avg = calc_average(run16)
run17_avg = calc_average(run17)
run15_var = calc_variance(run15, run15_avg)
run16_var = calc_variance(run16, run16_avg)
run17_var = calc_variance(run17, run17_avg)
run15_skew = calc_skewness(run15, run15_avg, run15_var)
run16_skew = calc_skewness(run16, run16_avg, run16_var)
run17_skew = calc_skewness(run17, run17_avg, run17_var)
run15_kurt = calc_kurtosis(run15, run15_avg, run15_var)
run16_kurt = calc_kurtosis(run16, run16_avg, run16_var)
run17_kurt = calc_kurtosis(run17, run17_avg, run17_var)
ten_k_b_mean_var = (run15_var + run16_var + run17_var) / 3
ten_k_b_std = calc_std_dev(run15_var, run16_var, run17_var)
ten_k_b_corrected = ten_k_b_mean_var - amp_baseline
ten_k_b_skew = (run15_skew + run16_skew + run17_skew) / 3
ten_k_b_skew_std = calc_std_dev(run15_skew, run16_skew, run17_skew)
ten_k_b_kurt = (run15_kurt + run16_kurt + run17_kurt) / 3
ten_k_b_kurt_std = calc_std_dev(run15_kurt, run16_kurt, run17_kurt)

results.append((10000, ten_k_b_corrected, ten_k_b_std, ten_k_b_mean_var, ten_k_b_skew, ten_k_b_skew_std, ten_k_b_kurt, ten_k_b_kurt_std))

# Johnson Noise (R_in = 100k Ohm)
run18_avg = calc_average(run18)
run19_avg = calc_average(run19)
run20_avg = calc_average(run20)
run18_var = calc_variance(run18, run18_avg)
run19_var = calc_variance(run19, run19_avg)
run20_var = calc_variance(run20, run20_avg)
run18_skew = calc_skewness(run18, run18_avg, run18_var)
run19_skew = calc_skewness(run19, run19_avg, run19_var)
run20_skew = calc_skewness(run20, run20_avg, run20_var)
run18_kurt = calc_kurtosis(run18, run18_avg, run18_var)
run19_kurt = calc_kurtosis(run19, run19_avg, run19_var)
run20_kurt = calc_kurtosis(run20, run20_avg, run20_var)
hundred_k_mean_var = (run18_var + run19_var + run20_var) / 3
hundred_k_std = calc_std_dev(run18_var, run19_var, run20_var)
hundred_k_corrected = hundred_k_mean_var - amp_baseline
hundred_k_skew = (run18_skew + run19_skew + run20_skew) / 3
hundred_k_skew_std = calc_std_dev(run18_skew, run19_skew, run20_skew)
hundred_k_kurt = (run18_kurt + run19_kurt + run20_kurt) / 3
hundred_k_kurt_std = calc_std_dev(run18_kurt, run19_kurt, run20_kurt)

results.append((100000, hundred_k_corrected, hundred_k_std, hundred_k_mean_var, hundred_k_skew, hundred_k_skew_std, hundred_k_kurt, hundred_k_kurt_std))

# Johnson Noise (R_in = 1M Ohm, gain_200)
run21_avg = calc_average(run21)
run22_avg = calc_average(run22)
run23_avg = calc_average(run23)
run21_var = calc_variance(run21, run21_avg)
run22_var = calc_variance(run22, run22_avg)
run23_var = calc_variance(run23, run23_avg)
run21_skew = calc_skewness(run21, run21_avg, run21_var)
run22_skew = calc_skewness(run22, run22_avg, run22_var)
run23_skew = calc_skewness(run23, run23_avg, run23_var)
run21_kurt = calc_kurtosis(run21, run21_avg, run21_var)
run22_kurt = calc_kurtosis(run22, run22_avg, run22_var)
run23_kurt = calc_kurtosis(run23, run23_avg, run23_var)
one_M_mean_var = (run21_var + run22_var + run23_var) / 3
one_M_std = calc_std_dev(run21_var, run22_var, run23_var)
one_M_corrected = one_M_mean_var - amp_baseline_200
one_M_skew = (run21_skew + run22_skew + run23_skew) / 3
one_M_skew_std = calc_std_dev(run21_skew, run22_skew, run23_skew)
one_M_kurt = (run21_kurt + run22_kurt + run23_kurt) / 3
one_M_kurt_std = calc_std_dev(run21_kurt, run22_kurt, run23_kurt)

results.append((1000000, one_M_corrected, one_M_std, one_M_mean_var, one_M_skew, one_M_skew_std, one_M_kurt, one_M_kurt_std))

# ============================================================================
# PRINT STATEMENTS (GUARDED)
# ============================================================================

if __name__ == "__main__":
    # ============================================================================
    # OUTPUT: Amplifier Noise Baseline (gain_300, R_in = 1 Ohm)
    # ============================================================================
    print("=" * 60)
    print("AMPLIFIER NOISE BASELINE (gain_300, R_in = 1 Ohm)")
    print("=" * 60)
    print("  Run 0: var =", run0_var, " skew =", run0_skew, " kurt =", run0_kurt)
    print("  Run 1: var =", run1_var, " skew =", run1_skew, " kurt =", run1_kurt)
    print("  Run 2: var =", run2_var, " skew =", run2_skew, " kurt =", run2_kurt)
    print("  Baseline variance:", amp_baseline, "+/-", amp_std, "V^2")
    print("  Skewness:", amp_skew, "+/-", amp_skew_std, "(expect 0)")
    print("  Kurtosis:", amp_kurt, "+/-", amp_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 10 Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 10 Ohm)")
    print("=" * 60)
    print("  Run 3: var =", run3_var, " skew =", run3_skew, " kurt =", run3_kurt)
    print("  Run 4: var =", run4_var, " skew =", run4_skew, " kurt =", run4_kurt)
    print("  Run 5: var =", run5_var, " skew =", run5_skew, " kurt =", run5_kurt)
    print("  Mean variance:", ten_ohm_mean_var, "+/-", ten_ohm_std, "V^2")
    print("  Corrected (baseline subtracted):", ten_ohm_corrected, "V^2")
    print("  Skewness:", ten_ohm_skew, "+/-", ten_ohm_skew_std, "(expect 0)")
    print("  Kurtosis:", ten_ohm_kurt, "+/-", ten_ohm_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 100 Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 100 Ohm)")
    print("=" * 60)
    print("  Run 6: var =", run6_var, " skew =", run6_skew, " kurt =", run6_kurt)
    print("  Run 7: var =", run7_var, " skew =", run7_skew, " kurt =", run7_kurt)
    print("  Run 8: var =", run8_var, " skew =", run8_skew, " kurt =", run8_kurt)
    print("  Mean variance:", hundred_ohm_mean_var, "+/-", hundred_ohm_std, "V^2")
    print("  Corrected (baseline subtracted):", hundred_ohm_corrected, "V^2")
    print("  Skewness:", hundred_ohm_skew, "+/-", hundred_ohm_skew_std, "(expect 0)")
    print("  Kurtosis:", hundred_ohm_kurt, "+/-", hundred_ohm_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 1k Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 1k Ohm)")
    print("=" * 60)
    print("  Run 9: var =", run9_var, " skew =", run9_skew, " kurt =", run9_kurt)
    print("  Run 10: var =", run10_var, " skew =", run10_skew, " kurt =", run10_kurt)
    print("  Run 11: var =", run11_var, " skew =", run11_skew, " kurt =", run11_kurt)
    print("  Mean variance:", one_k_mean_var, "+/-", one_k_std, "V^2")
    print("  Corrected (baseline subtracted):", one_k_corrected, "V^2")
    print("  Skewness:", one_k_skew, "+/-", one_k_skew_std, "(expect 0)")
    print("  Kurtosis:", one_k_kurt, "+/-", one_k_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 10k Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 10k Ohm)")
    print("=" * 60)
    print("  Run 12: var =", run12_var, " skew =", run12_skew, " kurt =", run12_kurt)
    print("  Run 13: var =", run13_var, " skew =", run13_skew, " kurt =", run13_kurt)
    print("  Run 14: var =", run14_var, " skew =", run14_skew, " kurt =", run14_kurt)
    print("  Mean variance:", ten_k_mean_var, "+/-", ten_k_std, "V^2")
    print("  Corrected (baseline subtracted):", ten_k_corrected, "V^2")
    print("  Skewness:", ten_k_skew, "+/-", ten_k_skew_std, "(expect 0)")
    print("  Kurtosis:", ten_k_kurt, "+/-", ten_k_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 10k Ohm)* NOTE! Repeated accidentally
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 10k Ohm*)")
    print("=" * 60)
    print("  Run 15: var =", run15_var, " skew =", run15_skew, " kurt =", run15_kurt)
    print("  Run 16: var =", run16_var, " skew =", run16_skew, " kurt =", run16_kurt)
    print("  Run 17: var =", run17_var, " skew =", run17_skew, " kurt =", run17_kurt)
    print("  Mean variance:", ten_k_b_mean_var, "+/-", ten_k_b_std, "V^2")
    print("  Corrected (baseline subtracted):", ten_k_b_corrected, "V^2")
    print("  Skewness:", ten_k_b_skew, "+/-", ten_k_b_skew_std, "(expect 0)")
    print("  Kurtosis:", ten_k_b_kurt, "+/-", ten_k_b_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 100k Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 100k Ohm)")
    print("=" * 60)
    print("  Run 18: var =", run18_var, " skew =", run18_skew, " kurt =", run18_kurt)
    print("  Run 19: var =", run19_var, " skew =", run19_skew, " kurt =", run19_kurt)
    print("  Run 20: var =", run20_var, " skew =", run20_skew, " kurt =", run20_kurt)
    print("  Mean variance:", hundred_k_mean_var, "+/-", hundred_k_std, "V^2")
    print("  Corrected (baseline subtracted):", hundred_k_corrected, "V^2")
    print("  Skewness:", hundred_k_skew, "+/-", hundred_k_skew_std, "(expect 0)")
    print("  Kurtosis:", hundred_k_kurt, "+/-", hundred_k_kurt_std, "(expect 3)")

    # ============================================================================
    # OUTPUT: Amplifier Noise Baseline (gain_200, R_in = 1 Ohm)
    # ============================================================================
    print("\n" + "=" * 60)
    print("AMPLIFIER NOISE BASELINE (gain_200, R_in = 1 Ohm)")
    print("=" * 60)
    print("  Run 24: var =", run24_var, " skew =", run24_skew, " kurt =", run24_kurt)
    print("  Run 25: var =", run25_var, " skew =", run25_skew, " kurt =", run25_kurt)
    print("  Run 26: var =", run26_var, " skew =", run26_skew, " kurt =", run26_kurt)
    print("  Baseline variance:", amp_baseline_200, "+/-", amp_std_200, "V^2")
    print("  Skewness:", amp_skew_200, "+/-", amp_skew_std_200, "(expect 0)")
    print("  Kurtosis:", amp_kurt_200, "+/-", amp_kurt_std_200, "(expect 3)")

    # ============================================================================
    # OUTPUT: Johnson Noise (R_in = 1M Ohm, gain_200)
    # ============================================================================
    print("\n" + "=" * 60)
    print("JOHNSON NOISE (R_in = 1M Ohm)")
    print("=" * 60)
    print("  Run 21: var =", run21_var, " skew =", run21_skew, " kurt =", run21_kurt)
    print("  Run 22: var =", run22_var, " skew =", run22_skew, " kurt =", run22_kurt)
    print("  Run 23: var =", run23_var, " skew =", run23_skew, " kurt =", run23_kurt)
    print("  Mean variance:", one_M_mean_var, "+/-", one_M_std, "V^2")
    print("  Corrected (baseline subtracted):", one_M_corrected, "V^2")
    print("  Skewness:", one_M_skew, "+/-", one_M_skew_std, "(expect 0)")
    print("  Kurtosis:", one_M_kurt, "+/-", one_M_kurt_std, "(expect 3)")