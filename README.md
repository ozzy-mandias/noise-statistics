# Johnson Noise as an Experimental Test of the Jaynes Maximum-Entropy Framework

San José State University · Spring 2026
Author: Akhilan Celeis Raja · Advisor: Dr. Peter Beyersdorf

## Quick Links

- **Paper:** [`paper/main.tex`](paper/main.tex)
- **Data:** [`data/`](data/)
- **Analysis scripts:** [`analysis/`](analysis/)
- **Figures:** [`plots/`](plots/)

## What This Is

Source code, data, and analysis for a paper testing the Jaynes
(1957) maximum-entropy interpretation of statistical mechanics
through Johnson noise measurements across 77–300 K.

## Reproducing the Figures

All scripts read from `data/` and write to `plots/`.

```bash
python analysis/calc_moments.py           # → moments table (printed)
python analysis/plot_histograms.py        # → plots/histograms.png
python analysis/plot_psd_vs_frequency.py  # → plots/psd_vs_freq.png
python analysis/plot_moments.py           # → plots/moments.png
python analysis/extract_kB.py            # → plots/kB_extraction.png
```

## Directory Structure

```
├── analysis/              Analysis and plotting scripts
│   ├── calc_moments.py        Statistical moments for each resistor
│   ├── calc_spectra.py        PSD computation from voltage traces
│   ├── extract_kB.py          k_B extraction from variance vs R
│   ├── plot_histograms.py     Amplitude distributions + Gaussian fits
│   ├── plot_moments.py        Skewness/kurtosis vs resistance
│   └── plot_psd_vs_frequency.py   PSD vs frequency for all resistors
│
├── data/
│   ├── amp_noise/             Amplifier baseline (10 Ω, noise subtraction)
│   └── johnson_noise/         Voltage traces by resistor value
│       ├── 10_ohms/
│       ├── 100_ohms/
│       ├── 1k_ohms/
│       ├── 10k_ohms/
│       ├── 100k_ohms/
│       └── 1M_ohm/
│
├── plots/                 Generated figures for the paper
│
├── paper/                 LaTeX source
│   ├── main.tex
│   ├── refs.bib
│   └── bridge_diagram.tex
│
├── sr1_scripts/           SR1 audio analyzer utilities
│
└── README.md
```

## Data Format

Each trace is a CSV exported from the GW-INSTEK GDS-1052-U.
Folder names encode the run metadata:

```
LOG_<R>_run_<N>_gain_<G2>_<T>K
```

Example: `LOG_1_kOHM_run_1_gain_300_294.7K` is run 1 of the
1 kΩ resistor at gain G₂ = 300 and temperature 294.7 K.

## Status

| Component | Status |
|---|---|
| Room-temperature phenomenology | Complete |
| k_B from resistance dependence | 1.2% agreement with CODATA |
| Temperature-dependent measurements (77–300 K) | Pending |
| Paper | Theory and appendices written; results awaiting data |

## License

CC BY-NC-ND 4.0