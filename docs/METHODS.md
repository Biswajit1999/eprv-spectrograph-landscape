# Methods and evidence rules

## Research question

What have the main stabilized EPRV spectrographs achieved, what is their
current operational state, and which obstacles remain before approximately
10 cm/s Doppler measurements can be sustained over the multi-year cadence
needed for temperate terrestrial planets?

## Inclusion protocol

An instrument is included in v0.1 when it satisfies all of the following:

1. It is a fibre-fed or equivalently stabilized high-resolution
   spectrograph built substantially for exoplanet radial velocities.
2. A primary instrument or performance paper is publicly identifiable.
3. A consortium, observatory, or facility page supports a dated status.
4. Its inclusion adds a distinct generation, wavelength domain,
   calibration approach, or operational lesson.

The list is intentionally representative rather than exhaustive. Legacy
instruments without a strong EPRV design role and general-purpose
high-resolution spectrographs are outside v0.1.

## Evidence hierarchy

Facts are classified before comparison:

- `design_requirement`: a proposed or specified goal; not achieved.
- `laboratory_calibration`: internal calibration performance without a star.
- `commissioning_report`: an early system or subsystem result.
- `on_sky_stability`: a stellar or solar observation, necessarily including
  photon, atmospheric, analysis, and astrophysical contributions.
- `not_comparably_reported`: no safe like-for-like number was extracted.

The code refuses uncontrolled labels such as “best.” The free-text
performance column is retained because reducing heterogeneous experiments
to a single numeric column would create a false ranking.

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

`eprv-landscape build` validates the schema, writes three derived CSV
summaries, two plots, and `results/manifest.json`. Every plotted number is
read from `data/instruments.csv`; no values are embedded in plotting code.
