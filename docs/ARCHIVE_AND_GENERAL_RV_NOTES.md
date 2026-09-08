# Archive and general-purpose RV reading notes

This chapter follows 28 selected sources for six instruments outside the
stabilized detailed core. Their archives are scientifically valuable, but their
measurement architectures and current modes differ. No common precision score
is calculated.

## HIRES

HIRES established iodine-cell Doppler work on Keck. The historical 3 m/s method
result belongs to its original detector and modelling context. Later public
catalogs corrected nightly systematics, and the 2025 catalog extends spectra
through March 2023. Long-baseline survey results combine instrumental, stellar
and model terms rather than measuring an isolated instrument floor.

Current planning says HIRES will be decommissioned no earlier than the end of
2027B; the date depends on ZShooter readiness and KPF stability. A useful archive
study therefore needs detector, template, reduction and catalog-version fields
for every velocity.

## UVES

UVES is a versatile slit-fed two-arm spectrograph with an iodine cell, not a
dedicated stabilized EPRV instrument. Asteroid and iodine comparisons have shown
setting-dependent wavelength-scale structure. Absolute velocity accuracy,
intra-order distortion and differential stellar precision remain separate
measurements.

ESO offers UVES in Period 118. That dated availability does not make two decades
of arms, slits, settings and detector configurations homogeneous. An archive
audit should group every exposure by configuration before fitting corrections.

## CHIRON

CHIRON offers several resolution modes, a fibre feed and an iodine option. The
design, commissioning and as-built papers establish its optical architecture and
early performance, but do not support one precision value across modes.

The CTIO page maintains manuals, monitoring and scheduling links but does not
provide a dated 2026 semester statement. A future mode comparison should match
targets and signal-to-noise, separate iodine and non-iodine paths, and hold out
whole observing runs.

## FIES

FIES began as a general stellar spectrograph. Octagonal fibres, a controlled
grating environment and calibration work improved its RV use. A seven-point
12-day sequence reported 3.3 m/s RMS, while a separate ten-month sigma Draconis
study reported about 5 m/s. These are not contradictory because their samples
and baselines differ.

Technical work identifies exposure-meter placement and wavelength-solution
complexity as error terms. The March 2026 NOT schedule confirms current FIES
use. A replay should choose wavelength-model complexity before evaluating
held-out stellar nights.

## GHOST

GHOST is operational for broad high-resolution spectroscopy at Gemini South.
Its performance paper documents 348–1061 nm coverage and two resolution modes.
The later PRV roadmap estimates a 1–10 m/s range, but 2026A material says the
simultaneous-calibration PRV mode is not offered.

The website therefore separates general instrument operation from specialist
mode availability. Roadmap estimates remain design evidence until held-out
standard-star and calibration tests support an offered facility specification.

## Veloce

Veloce grew from the Rosso channel into a three-arm system. Its sub-m/s language
was a design objective. Community verification and the 2024 upgrade record new
channels, while the 2026 reduction paper identifies overlapping fibre images as
a limit on extraction and wavelength calibration.

The new pipeline is explicitly intended for non-RV science. The current AAT page
offers Veloce Rosso on a shared-risk basis. A future joint-profile extraction
test should measure cross-talk on held-out orders and verify that injected line
shifts and line shapes are preserved.

## Evidence boundary

The machine-readable sources are `data/hires_papers.csv`, `data/uves_papers.csv`,
`data/chiron_papers.csv`, `data/fies_papers.csv`, `data/ghost_papers.csv` and
`data/veloce_papers.csv`. Paper and facility links are available in each website
profile. No third-party figure or substantial source text is copied.
