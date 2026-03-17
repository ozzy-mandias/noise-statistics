import csv

with open("data/frequency_response/frequency_response_gain_300.TXT") as f:
    lines = [l.strip() for l in f if not l.startswith("//") and l.strip()]

print("Total data points:", len(lines))
print("First 3:", lines[:3])
print("Last 3:", lines[-3:])