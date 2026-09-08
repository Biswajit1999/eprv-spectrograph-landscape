# HARPS reading note: calibration structure and instrument eras

**Reviewed:** 7 September 2026  
**Scope:** Six selected technical, calibration and status sources from 2003–2026.
This is not a complete bibliography of HARPS planet surveys or archival uses.

## Direct answer

HARPS is a fibre-fed, cross-dispersed echelle spectrograph on the ESO 3.6 m
telescope at La Silla. The commissioning description gives a resolving power of
about 115,000 over 380–690 nm and explains the design choices that made the
instrument stable: a vacuum enclosure, tightly controlled temperature and a
simultaneous reference fibre. These properties are part of the measurement
system; none is, by itself, a statement of stellar radial-velocity accuracy.

The selected literature shows three different questions being answered. The
2003 commissioning sequences tested short-term instrumental tracking and early
stellar observations. Later laser-frequency-comb and Fabry–Pérot work examined
local wavelength-solution and line-profile structure. Hardware interventions in
2015 and 2026 created new observing eras. A long-baseline analysis must therefore
retain calibration method, pipeline version and hardware era instead of treating
the archive as one stationary time series.

ESO reports that HARPS returned to operations on 20 June 2026 after detector,
electronics, cooling and HAM-fibre work. A 3 July notice says the atmospheric-
dispersion corrector was out of operation and recommends observations at low
airmass. The same page says a final performance report will follow. This supports
an operational-status statement with a caveat; it does not support a final claim
about post-upgrade RV performance.

## Reading path

### 1. Commissioning: separate reference tracking from stellar scatter

Mayor et al. (2003) describe the two-fibre layout, 72 echelle orders and the
environmental controls. In a repeated ThAr test, subtracting the common response
of the two fibres produced a dispersion at the expected photon-noise level; the
authors report instrumental-drift tracking at 0.1 m/s RMS. That is a simultaneous-
reference result, not a multi-year stellar RMS.

The same report gives a useful on-sky comparison. A seven-hour sequence of 420
spectra of alpha Centauri B had 0.51 m/s dispersion. The authors estimated a
0.44 m/s contribution from stellar oscillation modes and a 0.17 m/s photon-noise
term per measurement. Their quadrature subtraction yielded a 0.26 m/s noise
level. A separate nine-point, four-month check on HD 83443 had 1.7 m/s residual
dispersion around a known orbit. The sampling and targets differ, so these
numbers should not be collapsed into one “HARPS precision.”

[Commissioning article](https://www.eso.org/sci/publications/messenger/archive/no.114-dec03/messenger-no114-20-24.pdf)

### 2. Frequency-comb comparison: global residuals can hide local structure

Molaro et al. (2013) used a prototype laser frequency comb to produce a solar
atlas from reflected lunar light. Comparing the comb solution with the standard
ThAr solution exposed S-shaped distortions within orders, reaching roughly
plus or minus 40 m/s in the stated comparison. This is a local wavelength-scale
difference. It must not be presented as a 40 m/s error in every stellar RV;
different lines and epochs weight the detector differently.

[Frequency-comb solar atlas](https://arxiv.org/abs/1310.5087)

### 3. The 2015 fibre exchange: an improvement can also create a discontinuity

Lo Curto et al. (2015) report replacement of circular fibres with octagonal
fibres to improve scrambling. They measured about 40% higher throughput at
550 nm and found an RV offset across the intervention. Crucially, the offset
depended on the star and its spectral properties. One global step correction is
therefore not guaranteed to transfer across spectral types, masks or line sets.

[ESO Messenger fibre report](https://www.eso.org/public/archives/messengers/pdf/messenger_0162.pdf)

### 4. ThAr plus Fabry–Pérot: wavelength solutions belong to an era

Cersullo et al. (2019) use ThAr line positions to anchor the absolute solution
and a Fabry–Pérot etalon to supply dense relative information. Their analysis of
15 years of calibration data treats the periods before and after the 2015 fibre
change separately. That is the correct conceptual model for the archive: a
calibration is associated with an instrument configuration and cannot be assumed
to bridge a hardware boundary unchanged.

[Wavelength-calibration paper](https://arxiv.org/abs/1901.03294)

### 5. Line-spread function: a target is not an achieved stellar RMS

Milaković and Jethwa (2020) model HARPS line profiles from laser-frequency-comb
exposures in two detector dimensions and as a function of line intensity. Their
discussion places the work in the context of a wavelength scale precise enough
for approximately 3 cm/s Earth-analogue signals. That value is a motivating
scale. The paper does not demonstrate a 3 cm/s long-baseline stellar time series.
Its practical lesson is that fitting a symmetric or spatially invariant line
profile can leave structured calibration residuals.

[Line-profile paper](https://arxiv.org/abs/2011.03391)

### 6. The 2026 change: status is known before final performance is known

ESO’s dated notices record detector, electronics, cooling and fibre changes,
then a return to normal operations. Because several coupled subsystems changed,
the post-2026 system should be treated as a new measurement era. Until the final
characterisation is public, claims should be limited to the documented work and
operational caveats.

[Current ESO notices](https://www.eso.org/sci/facilities/lasilla/instruments/harps/news.html)

## What can be concluded

- HARPS commissioning demonstrated sub-m/s short-term measurements in specific
  reference and stellar sequences, with explicitly different noise terms.
- Dense calibrators revealed detector-position-dependent wavelength structure
  that a global residual statistic could conceal.
- The 2015 fibre intervention improved throughput and scrambling but introduced
  a star-dependent discontinuity.
- Calibration and RV products should carry an explicit instrument-era label.
- The 2026 configuration has documented operational notices, but final public
  post-upgrade performance was not available in the checked source.

## Future analysis question

### Question

Can a hierarchical transfer model estimate star-dependent offsets across the
2015 and 2026 boundaries while preserving low-amplitude Keplerian signals?

### Minimum defensible study

1. Define eras only from dated hardware, calibration and pipeline records.
2. Select stable stars spanning spectral type, line width, mask and signal-to-
   noise, with observations on both sides of a boundary.
3. Compare one global offset, independent star offsets and a partially pooled
   model whose predictors are defined before viewing the held-out result.
4. Hold out complete stars and contiguous time blocks, rather than random rows.
5. Inject sinusoids before correction and measure amplitude and phase recovery.
6. Report results by era and target; do not publish one pooled RMS as proof of
   transfer.

This is a future analysis question. It is not completed research, a publication
claim, or evidence that the necessary post-2026 products are public.

## Machine-readable records

The selected sources and the context attached to each numerical statement are
in `data/harps_papers.csv`. The website dossier and future-analysis boundary
are in `data/instrument_dossiers.json`.
