# EXPRES reading note: from design targets to long-baseline corrections

**Reviewed:** 7 September 2026  
**Scope:** 13 selected primary papers from 2016–2026 plus Lowell Observatory's
current observer material. This is a structured reading path, not a complete
bibliography of every paper that has used EXPRES.

## Direct answer

EXPRES is a useful case study because its literature makes the hierarchy of
precision unusually visible. The 2016 paper set an instrument design target of
15 cm/s and an intended on-sky scale better than 30 cm/s. The 2020 verification
paper reported calibration precision better than 10 cm/s in its stated test,
while explicitly excluding photon noise and stellar variability. The first
pipeline paper then reported a 0.3 m/s formal error at per-pixel S/N 250 and a
0.895 m/s residual RMS for 51 Peg. Those numbers are not contradictory: they
measure different parts of the observing and inference chain.

The scientific emphasis subsequently moved from short-term precision toward
wavelength models, photospheric variability, cross-instrument solar comparison,
and long-baseline instrument state. The most consequential recent result in this
reading set is Zhao et al. (2026): a coherent 2.8 m/s trough-to-peak drift was
found around a period of larger temperature variations near January 2022. Their
regression using echellogram geometry, laser-comb line shapes, and telemetry
reduced the solar trend RMS from 1.32 to 0.43 m/s. That paper does not make the
problem “solved”; it creates a concrete validation question about transfer
across instrument eras and preservation of weak planetary signals.

## Reading path

### 1. Design and error budget

Jurgenson et al. (2016) describe the fiber-fed echelle design for the 4.3 m
Lowell Discovery Telescope. Environmental control, image stabilization,
wavelength calibration and analysis are treated as parts of one error budget.
The quoted 15 cm/s instrument and better-than-30 cm/s on-sky values are targets,
not achieved multi-year measurements. [Primary paper](https://arxiv.org/abs/1606.04413)

### 2. Commissioning and reduction

Blackman et al. (2020) test the calibration, illumination, detector and observing
subsystems. The reported better-than-10 cm/s calibration result is deliberately
narrower than an end-to-end stellar measurement. [Primary paper](https://arxiv.org/abs/2003.08852)

Petersburg et al. (2020) document the extended flat, flat-relative optimal
extraction, chromatic barycentric correction, chromatic calibration offsets and
laser-frequency-comb wavelength solution. Their 51 Peg demonstration has a
0.895 m/s residual RMS; the formal single-measurement uncertainty reaches
0.3 m/s at per-pixel S/N 250. [Primary paper](https://arxiv.org/abs/2003.08851)

Brewer et al. (2020) use the known HD 3651 system as an on-sky check and report
a 58 cm/s residual RMS over roughly six months. This is strong target-specific
evidence, but it is not a universal or multi-year instrument floor.
[Primary paper](https://arxiv.org/abs/2006.02303)

### 3. Wavelength calibration and stellar spectra

Zhao et al. (2021) present Excalibur, a low-dimensional non-parametric wavelength
model. Laser-comb calibration residual RMS is reported as roughly five times
lower than the exposure-by-exposure polynomial approach, while the HD 34411
stellar RMS changes from 1.17 to 1.05 m/s. The differing improvement sizes are a
useful reminder that wavelength calibration is only one term in the final
stellar velocity. [Primary paper](https://arxiv.org/abs/2010.13786)

The first EXPRES Stellar-Signals Project note defines common spectroscopic,
velocity, activity-indicator and photometric data for four stars. The second
paper compares 22 methods on common EXPRES data. Nearly every method improves
on classic linear decorrelation, but no method consistently reaches sub-m/s
RMS and the corrected velocities disagree. The authors therefore call for
interpretable models, better cadence, known injections and signal-preservation
tests. [Data note](https://doi.org/10.3847/2515-5172/abb8d0) ·
[Method comparison](https://arxiv.org/abs/2201.10639)

### 4. Solar comparison and physically motivated corrections

The four-instrument solar comparison reports 15–30 cm/s residual intra-day
scatter among HARPS, HARPS-N, EXPRES and NEID. Because the observations are
simultaneous, common solar variability can be separated from instrument-specific
behaviour more directly than in unrelated stellar time series. The result does
not by itself establish long-term absolute accuracy.
[Primary paper](https://arxiv.org/abs/2309.03762)

Siegel et al. (2024) develop a Rotation-Convection model using flux information
and the relative velocity of strongly and weakly absorbed wavelengths. It brings
the HD 26965 activity signal to the m/s level in HARPS, EXPRES and NEID data.
Transfer to other activity patterns and preservation of weak planets remain
important tests. [Primary paper](https://arxiv.org/abs/2408.07121)

### 5. The long-baseline problem

Zhao et al. (2026) analyse seven years of data and track two-dimensional shifts,
scaling and rotation of the echellogram, laser-comb line-bisector spans and
environmental telemetry. The reported correction lowers the solar trend RMS
from 1.32 to 0.43 m/s, reduces aggregate scatter across 12 quiet stars by 26%,
and doubles sensitivity to low-amplitude injected planets in their simulations.
It also removes a spurious rho Coronae Borealis d signal. These results motivate
era-aware held-out validation rather than a random exposure split.
[Primary paper](https://arxiv.org/abs/2601.02296)

Shahaf & Zackay (2026) take a complementary spectral-factorization approach,
recovering principal spectra and time-dependent kernels with short-time Fourier
transforms and singular-value decomposition. Tests on EXPRES observations of
HD 34411 and tau Ceti reach an approximately 30 cm/s instrumental scale in the
reported analysis. The velocities are relative, and independent transfer tests
remain necessary. [Journal article](https://doi.org/10.1093/mnras/stag334)

## Future analysis question

### Era-aware EXPRES correction audit with planet-preservation tests

This question is derived from published limitations. It is not completed
research, a publication claim, or an endorsed instrument programme.

**Question:** Can a correction learned from instrument-state diagnostics remain
valid across maintenance and temperature regimes while preserving low-amplitude
Keplerian signals?

1. Align science and solar velocities with comb image shifts, scale, rotation,
   line-bisector spans, telemetry and maintenance dates.
2. Define instrument eras before fitting and hold out complete time blocks plus
   at least one era.
3. Establish a small interpretable regression baseline before comparing nonlinear
   alternatives on identical folds.
4. Inject Keplerian signals before correction over a grid of period, phase and
   semi-amplitude; measure amplitude bias, recovery and false positives.
5. Produce per-exposure state flags, correction uncertainty and an
   out-of-distribution warning.
6. Reproduce the published solar and quiet-star checks before any science claim.

An appropriate first message to the team would be:

> I reviewed the design, commissioning pipeline, wavelength-calibration,
> stellar-signal comparisons and the seven-year systematics study. I would like
> to test an era-held-out, injection-recovery extension of the published
> instrument-state correction. Before building against science products, which
> diagnostics can be shared and which validation case would be most useful to
> the team?

## Reusable standard for later instrument notes

Future full notes should contain: instrument history; current dated status;
design values separated from achieved results; a paper-by-paper chronology;
within-paper numerical comparisons; unresolved limitations; a project question;
required data; validation tests; and an explicit statement distinguishing a
future analysis question from the source authors' conclusions.

The machine-readable version is in `data/instrument_dossiers.json`; the selected
paper table is `data/expres_papers.csv`; and the paired values behind the original
figure are in `data/expres_metrics.csv`.
