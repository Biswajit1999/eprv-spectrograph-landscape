# Methods and evidence rules

## Research question

What have the main stabilized EPRV spectrographs achieved, what is their
current operational state, and which obstacles remain before approximately
10 cm/s Doppler measurements can be sustained over the multi-year cadence
needed for temperate terrestrial planets?

## Inclusion protocol

An instrument is included in the detailed comparison when it satisfies all of the following:

1. It is a fibre-fed or equivalently stabilized high-resolution
   spectrograph built substantially for exoplanet radial velocities.
2. A primary instrument or performance paper is publicly identifiable.
3. A consortium, observatory, or facility page supports a dated status.
4. Its inclusion adds a distinct generation, wavelength domain,
   calibration approach, or operational lesson.

The 19-system performance core follows Table 1 of Burt, Dumusque & Halverson
(2026), which covers current or upcoming visible instruments capable of at
least 1 m/s or near-infrared instruments capable of at least 3 m/s. ANDES and
G-CLEF are tracked as planned systems; PARAS-2 is a regional addition supported
by a 2024 on-sky paper. The list is not exhaustive. A physical instrument, an
observing mode, a detector upgrade and a pipeline version are not counted as
four independent instruments.

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

## Reproducibility

`eprv-landscape build` validates both source tables, writes four derived CSV
summaries, three plots, and `results/manifest.json`. Every plotted number is
read from committed CSV data; no values are embedded in plotting code.
