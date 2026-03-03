import os, math

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

# Storing amplifier noise data from ./data/amp_noise into variables that can be accessed here (3 runs of the same measurement)
run1 = load_run("data/amp_noise/LOG0001")
run0 = load_run("data/amp_noise/LOG0000")  
run2 = load_run("data/amp_noise/LOG0002")

# Storing Johnson noise data for a 10 Ohm resistor from ./data/amp_noise ... (3 runs of the same measurement)
run3 = load_run("data/johnson_noise/10_ohms/LOG0003")
run4 = load_run("data/johnson_noise/10_ohms/LOG0004")
run5 = load_run("data/johnson_noise/10_ohms/LOG0005")

# Functions for passing run data into to calculate statistical moments:

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
    
# Functions for error analysis:

# Standard Deviation
def calc_std_dev(v1, v2, v3):       #v1 is the variance of the first run, and so forth...
    average = (v1 + v2 + v3) / 3
    std_dev = math.sqrt(((v1 - average)**2 + (v2 - average)**2 + (v3 - average)**2) / 2) # IMPORTANT! The / 2 is the N-1 Bessel correction since N=3.
    return std_dev

# ============================================================================
# OUTPUT: Amplifier Noise Baseline (R_in = 1 Ohm)
# ============================================================================
run0_avg = calc_average(run0)
run1_avg = calc_average(run1)
run2_avg = calc_average(run2)
run0_var = calc_variance(run0, run0_avg)
run1_var = calc_variance(run1, run1_avg)
run2_var = calc_variance(run2, run2_avg)
amp_baseline = (run0_var + run1_var + run2_var) / 3
amp_std = calc_std_dev(run0_var, run1_var, run2_var)

print("=" * 60)
print("AMPLIFIER NOISE BASELINE (R_in = 1 Ohm)")
print("=" * 60)
print("  Run 0 variance:", run0_var, "V^2")
print("  Run 1 variance:", run1_var, "V^2")
print("  Run 2 variance:", run2_var, "V^2")
print("  Baseline (mean):", amp_baseline, "V^2")
print("  Uncertainty (std):", amp_std, "V^2")

# ============================================================================
# OUTPUT: Johnson Noise (R_in = 10 Ohm)
# ============================================================================
run3_avg = calc_average(run3)
run4_avg = calc_average(run4)
run5_avg = calc_average(run5)
run3_var = calc_variance(run3, run3_avg)
run4_var = calc_variance(run4, run4_avg)
run5_var = calc_variance(run5, run5_avg)
ten_ohm_mean_var = (run3_var + run4_var + run5_var) / 3
ten_ohm_std = calc_std_dev(run3_var, run4_var, run5_var)
ten_ohm_corrected = ten_ohm_mean_var - amp_baseline

print("\n" + "=" * 60)
print("JOHNSON NOISE (R_in = 10 Ohm)")
print("=" * 60)
print("  Run 3 variance:", run3_var, "V^2")
print("  Run 4 variance:", run4_var, "V^2")
print("  Run 5 variance:", run5_var, "V^2")
print("  Mean variance:", ten_ohm_mean_var, "V^2")
print("  Uncertainty (std):", ten_ohm_std, "V^2")
print("  Corrected (baseline subtracted):", ten_ohm_corrected, "V^2")