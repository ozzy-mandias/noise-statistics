# This file's purpose is to calculate the statistical moments of Johnson Noise

# Step 1 was to capture traces at certain settings (settings can be found in lab session logs)

# The oscilloscope (GW-INSTEK 1052-U) creates csv files, in the format:
# These files can be saved to a local machine

# Step 2 is writing a function that can be called when appropriate to load the data from multiple csv's
# into the appropriate data sctructure.

# Function load_run: takes a LOG folder path. It finds all the CSV files inside, calls load_trace on each one,
# and stacks the voltage arrays into one structure- either a list of arrays or a 2D array where each row is one trace.
# It also sanity-checks that all the headers match (same vertical scale, same sampling period).
# Returns the collection of traces plus the shared metadata.
def load_run(folder_path):

    return 0

# Function load_trace: takes a single CSV path. It reads the 16 header lines and pulls out the values
# (vertical scale, sampling period). Then it reads the remaining 4,000 integers,
# converts them to volts using the ADC formula you derived, builds the time array from the sampling period,
#  and returns all of it- the voltage array, the time array, and the header metadata as a dictionary or similar.
def load_trace(file_path):
    print("I received a trace from " + file_path)
    return 0


trace = load_trace("data/amp_noise/LOG0000/DS0000.CSV")