# Extreme-Precision Radial-Velocity Spectrograph Landscape

[![CI](https://github.com/Biswajit1999/eprv-spectrograph-landscape/actions/workflows/ci.yml/badge.svg)](https://github.com/Biswajit1999/eprv-spectrograph-landscape/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A source-traceable comparison of major optical and near-infrared
extreme-precision radial-velocity (EPRV) spectrographs: what they were
designed to achieve, what has actually been demonstrated, their status as
of 2 September 2026, and the engineering and astrophysical obstacles that
still separate selected sub-m/s measurements from routine detection of an
Earth analogue around a Sun-like star.

This repository deliberately does **not** publish a “best instrument”
ranking. A laboratory calibration residual, a short quiet-star sequence,
a single-visit uncertainty, and multi-year RV repeatability are different
quantities. The data model preserves that distinction.

## Scope

The v0.1 sample contains 13 influential or current systems: HARPS,
HARPS-N, ESPRESSO, EXPRES, NEID, KPF, CARMENES, HPF, SPIRou, NIRPS,
MAROON-X, HARPS3, and ANDES. Inclusion is based on direct relevance to
stabilized exoplanet Doppler spectroscopy, availability of a primary
instrument reference, and a dated official status source. It is a curated
landscape, not an exhaustive census.

## Reproduce

```bash
python -m pip install -e ".[dev]"
pytest -q
eprv-landscape build --data data/instruments.csv --out results
```

## Results

![Wavelength coverage](results/figures/wavelength_coverage.png)

![Resolution and spectral grasp](results/figures/resolution_vs_coverage.png)

The comparison shows an increasingly broad wavelength strategy: mature
optical instruments concentrate roughly between 380 and 930 nm, while
CARMENES, SPIRou, NIRPS, and HPF shift or extend the measurement into the
near infrared for cool stars and chromatic activity tests. ANDES aims to
join optical and NIR coverage at ELT collecting area, but its numerical
specifications remain requirements rather than achieved performance.

Operational maturity is not monotonic. HARPS underwent a major 2026
detector/fibre/pipeline upgrade; KPF is currently offline following a
vacuum-pump failure and has documented detector thermal excursions;
HARPS3 remains in commissioning. These are scientifically important state
variables, not footnotes to a timeless specification table.

Read the full synthesis in [docs/REPORT.md](docs/REPORT.md), the inclusion
and evidence rules in [docs/METHODS.md](docs/METHODS.md), and limitations
in [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

## What this does not claim

- It does not infer planet occurrence rates or detection completeness.
- It does not treat design goals as achieved performance.
- It does not compare instruments as though they observed the same star,
  cadence, wavelength region, and reduction pipeline.
- It is independent and is not endorsed by any listed observatory or
  instrument consortium.

## Data and licensing

The repository contains original tabular synthesis and plots, not copied
paper figures or observatory logos. External facts remain linked to their
primary sources. Code is MIT licensed; bibliographic metadata and factual
instrument specifications are cited rather than relicensed.
