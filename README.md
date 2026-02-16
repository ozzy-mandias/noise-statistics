# Noise Statistics as Information

San Jose State University, Department of Physics & Astronomy
Spring 2026

Advisor: Dr. Peter Beyersdorf

## What This Project Is About

Noise is usually treated as something to filter out. This project takes the opposite approach: we treat noise as a source of information about the physical system producing it. Starting from Johnson-Nyquist thermal noise, we measure voltage time-series data from resistors, compute statistical moments, and look for what the noise distribution can tell us about the underlying physics.

## Project Phases

**Phase I (Weeks 1-5):** Measure thermal noise voltage V(t) across different resistors, compute the first four statistical moments (mean, variance, skewness, kurtosis), and verify that the noise follows a Gaussian distribution as predicted by theory.

**Phase II (Weeks 6-10):** Look for deviations from ideal Gaussian noise that might reveal hidden physical structure in the system.

**Phase III (Weeks 11-15):** Develop uncertainty quantification frameworks using noise statistics as a measurement tool.

## Apparatus

- TeachSpin Noise Fundamentals (noise source and signal conditioning)
- GW-INSTEK GDS-1052-U oscilloscope (time-domain waveform capture, USB CSV export, 4,000 pts/trace)
- SR1 Audio Analyzer (spectral analysis where appropriate)

## Repository Structure

```
noise-statistics/
├── phase1/
├── phase2/
├── phase3/
├── analysis/
│   └── calc_moments.py
├── data/
│   └── raw/
├── docs/
│   └── session_logs/
├── .gitignore
├── LICENSE
└── README.md
```

## Data Naming Convention

Raw waveform files follow this pattern:

```
noise_V_R<value>_T<temp>K_<trial>.csv
```

Example: `noise_V_R100_T295K_003.csv` is the third trial of a 100 ohm resistor at 295 K.

## Key Physics

The variance of thermal noise voltage across a resistor is predicted by the Johnson-Nyquist relation:

⟨V²⟩ = 4 k_B T R Δf

where k_B is Boltzmann's constant, T is temperature, R is resistance, and Δf is the measurement bandwidth. For ideal thermal noise, the distribution should be Gaussian: the mean is zero, the variance encodes temperature and resistance, and the third and fourth moments (skewness and kurtosis) serve as diagnostics for deviations from that ideal.

## License

CC BY-NC-ND 4.0. See [LICENSE](LICENSE).
