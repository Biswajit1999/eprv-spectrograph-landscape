# HARPS-N reading note: wavelength solutions and a decade of solar data

**Reviewed:** 8 September 2026  
**Scope:** Six selected instrument, calibration, solar and current-status sources.
This is not a complete bibliography of HARPS-N exoplanet or atmosphere studies.

## Direct answer

HARPS-N is a fibre-fed, vacuum-enclosed, cross-dispersed echelle spectrograph on
the 3.58 m Telescopio Nazionale Galileo. The 2012 instrument paper reports
R ≈ 115,000 over 383–690 nm, two fibres, image scrambling and millikelvin-scale
temperature control. Its design choices limit illumination and environmental
drift; they do not remove stellar variability or make every pipeline version
equivalent.

The solar record is the more informative story. In the three-year release, an
ESPRESSO-derived reduction, stable ThAr-line selection and calibrations closer in
time reduced day-to-day scatter from 1.27 to 1.07 m/s across 34,550 spectra. The
authors estimate a 0.49 m/s wavelength-calibration term, while the remaining
solar series includes astrophysical variability. This is evidence that data
reduction was part of the limiting measurement, not proof of a 1.07 m/s
instrument floor.

The 2025 decade preprint analyses 13 years of wavelength solutions and releases
109,466 curated solar spectra after rejecting 30% of observations affected by
clouds, poor conditions or understood systematics. It reports a median daily RMS
of 0.49 m/s, a raw decade RMS of 2.95 m/s from the solar cycle, and 0.41 m/s after
modelling that long-term activity. These are three different statistics.

## Selected evidence

- **2012 design:** 0.3 m/s short-term and better-than-0.6 m/s long-term values
  appear in the instrument table; they must retain the paper's commissioning
  context. [Instrument paper](https://plone.unige.ch/HARPS-N/science-with-harps-n/publications/Cosentino_SPIE8446_66_2012.pdf)
- **2017 astro-comb:** a 16 GHz comb covered about 90 nm near 566 nm and enabled
  detector and intrapixel tests. It did not cover the full stellar band.
  [Comb paper](https://arxiv.org/abs/1705.07192)
- **2021 solar reduction:** local wavelength solutions could change by tens of
  m/s even though their combined effect on the final RV was smaller.
  [Three-year release](https://www.aanda.org/articles/aa/full_html/2021/04/aa39350-20/aa39350-20.html)
- **2023 cross-instrument test:** after time matching and accounting for binning,
  four solar instruments agreed with 0.15–0.30 m/s unexplained intraday scatter.
  This is not a multi-year floor. [Comparison](https://arxiv.org/abs/2309.03762)
- **2025 decade release:** the data definition includes explicit rejection and
  correction choices; any downstream result must preserve those masks.
  [Preprint](https://arxiv.org/abs/2510.27635)
- **Current status:** TNG AOT54 information says HARPS-N can be used normally in
  service or visitor mode and GIARPS is unrestricted.
  [TNG call](https://tngweb.tng.iac.es/call/info.html)

## Future analysis question

One possible analysis is an auditable solar quality mask. It would encode
weather, lamp, detector warm-up, drift, blaze and pipeline-version intervals as
separate flags; reproduce published sample counts; hold out a complete year;
and inject signals before curation to measure attenuation. Overlapping NEID days
would provide an external check on whether a residual is solar or local.

This is a future analysis question, dependent on released products and event
metadata. It is not completed research or a publication claim. Records are in
`data/harpsn_papers.csv` and
`data/instrument_dossiers.json`.
