# Measurement context in precision radial-velocity spectrograph comparisons

**Author:** Biswajit Jana
**Version:** 0.3.0
**Status:** research-software manuscript draft

## Abstract

Published radial-velocity performance values describe non-equivalent
experiments. This work assembles a dated comparison of 21 optical and
near-infrared spectrographs and 22 quantitative claims, separating engineering
requirements, calibration tests, internal uncertainties, stellar or solar
scatter and fitted residuals. The synthesis shows that selected sub-m/s on-sky
measurements coexist with persistent metre-per-second astrophysical and
measurement-system effects. A controlled synthetic Fisher-information study
additionally demonstrates that an R=100,000 to 150,000 increase improves the
ideal local uncertainty by 37.1% for 1 km/s intrinsic line widths but only
2.48% for 5 km/s widths under equal-photon assumptions. It proposes a minimum
reporting schema for future cross-instrument comparisons. The complete
analysis, instrument discussion,
limitations and references are maintained in [`docs/REPORT.md`](../docs/REPORT.md)
and the machine-readable evidence is in
[`data/performance_claims.csv`](../data/performance_claims.csv).

## Reproducibility statement

All figures are generated from committed CSV files. No third-party plots or
logos are included. Automated tests validate controlled vocabularies and
claim-to-instrument links. Seeded Poisson injection-recovery trials validate
the synthetic information calculation in its declared local regime. The
project does not independently re-reduce raw
spectra and does not claim instrument ranking or survey completeness.
