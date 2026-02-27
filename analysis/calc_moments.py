import os

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
    for folder in os.listdir(path):                         # Loop through LOG folders
        if folder.startswith("LOG"):                        # Skip .DS_Store and other non-data entries
            for file in os.listdir(path + "/" + folder):    # Loop through CSV files in each LOG folder
                if file.endswith(".CSV"):
                    vert_scale, sampling_period, voltages, time = load_trace(path + "/" + folder + "/" + file)
                    all_voltages.append(voltages)           # Append each trace's voltage array to the collection
    
    return all_voltages

all_voltages = load_run("data/amp_noise")               # Change hardcoded path to change which directory is passed to load_run

print(len(all_voltages))