# Methods and evidence rules

## Research question

What have the main stabilized EPRV spectrographs achieved, what is their
current operational state, and which obstacles remain before approximately
10 cm/s Doppler measurements can be sustained over the multi-year cadence
needed for temperate terrestrial planets?

## Two-layer inclusion protocol

The project separates discovery from quantitative comparison. The **broader
physical-instrument census** has four labelled tiers: dedicated PRV/EPRV
systems; general high-resolution instruments with published stellar-RV
evidence; historical prototypes or specialist systems; and funded,
construction, or commissioning projects. One row represents one physical
instrument. Networks such as NRES are split by physical site. A row may remain
`partially_verified`, but it must name every unresolved field.

The **performance core** applies the stricter rules below.

An instrument is included in the detailed comparison when it satisfies all of the following:

1. It is a fibre-fed or equivalently stabilized high-resolution
   spectrograph built substantially for exoplanet radial velocities.
2. A primary instrument or performance paper is publicly identifiable.
3. A consortium, observatory, or facility page supports a dated status.
4. Its inclusion adds a distinct generation, wavelength domain,
   calibration approach, or operational lesson.

The committed performance core contains **21 physical instruments** and uses
Table 1 of Burt, Dumusque & Halverson (2026) as its principal reference frame.
Planned systems and the regional PARAS-2 case are explicitly labelled rather
than implied to be homogeneous with operating instruments. The 22-row claim
table is larger than the instrument table because EXPRES has separate
laboratory-calibration and on-sky claims. The list is not exhaustive. A physical
instrument, an observing mode, a detector upgrade and a pipeline version are not
counted as four independent instruments.

## Evidence hierarchy

Facts are classified before comparison:

- `design_requirement`: a proposed or specified goal; not achieved.
- `laboratory_calibration`: internal calibration performance without a star.
- `commissioning_report`: an early system or subsystem result.
- `on_sky_stability`: a stellar or solar observation, necessarily including
  photon, atmospheric, analysis, and astrophysical contributions.
- `not_comparably_reported`: no safe like-for-like number was extracted.

The code refuses uncontrolled labels such as “best.” A numeric claim is stored
only with its metric, context, sample, baseline and caveat. Heterogeneous values
are never combined into a merit score.

## Specification extraction

Wavelength limits and resolving power are representative nominal modes.
Several instruments have multiple modes or separate arms; those details
are described in the report and sources. Plot coordinates are therefore
for orientation, not engineering acceptance tests.

## Status verification

Current status is taken from facility or consortium pages and stamped with
`status_as_of`. Status can change faster than journal literature; a row is
stale once its source has not been checked for 180 days. Historical
performance is never silently rewritten to match a current outage.

Conflicting official pages produce `status_conflict`, not an arbitrary choice.
“Installed and tested” produces `installed_testing`, not “operational.”

## Reproducibility

`eprv-landscape build` validates the quantitative source tables, writes four derived CSV
summaries, three plots, and `results/manifest.json`. Every plotted number is
read from committed CSV data; no values are embedded in plotting code.
`load_census` separately enforces unique physical identifiers, resolved facility
references, HTTPS sources, controlled inclusion tiers, and declared open fields.

## Controlled Doppler-information experiment

The literature synthesis is supplemented by one independently executed,
falsifiable experiment. A deterministic synthetic absorption-line ensemble is
broadened by intrinsic and instrumental Gaussian kernels while line equivalent
widths, velocity sampling and continuum photons per bin remain fixed. Local
Doppler information is calculated from the spectral gradient and validated by
seeded Poisson injection-recovery trials.

The predeclared null, equations, scenario table, acceptance boundary and
results are documented in `docs/DOPPLER_INFORMATION_STUDY.md`. The experiment
does not use the heterogeneous instrument rows as inputs and cannot support an
instrument ranking.
