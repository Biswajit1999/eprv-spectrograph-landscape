# ESPRESSO reading note: precision, accuracy and the science light path

**Reviewed:** 7 September 2026  
**Scope:** Seven selected instrument, calibration, science and status sources.
This is not a complete bibliography of ESPRESSO observing programmes.

## Direct answer

ESPRESSO combines a stabilized, fibre-fed spectrograph with the collecting area
of one or four VLT Unit Telescopes. Pepe et al. report resolving powers of about
140,000 or 190,000 in single-UT modes and about 70,000 with four UTs, over
roughly 378–789 nm. Their commissioning results separate the measured stellar
sequence from the inferred instrument contribution: better than 0.25 m/s during
one night and 0.50 m/s over several months, described as compatible with an
instrumental precision of 0.10 m/s. The last number is not a universal stellar
RMS.

The later reading path turns from precision to calibration accuracy. Comparisons
of ThAr, Fabry–Pérot and laser-comb solutions reveal structured wavelength
differences. A 2025 temporary iodine-cell experiment then tests a path closer to
the one followed by science light. It reports few-m/s wavelength accuracy and
less-than-0.20 m/s end-to-end RV stability in its stated experiment, while also
finding sensitivity to fibre-injection geometry. Accuracy and repeatability are
therefore separate axes, not competing estimates of one number.

## What each selected source adds

1. **Proxima, 2020.** Sixty-three 2019 spectra had a typical 0.26 m/s photon-
   noise uncertainty. Joint RV/activity modelling recovered Proxima b at
   11.218 ± 0.029 days. This is a planet-plus-activity inference, not a pure
   instrument test. [Paper](https://arxiv.org/abs/2005.12114)
2. **Instrument performance, 2021.** The one-night, several-month and inferred
   instrument values have different baselines and noise content.
   [Paper](https://arxiv.org/abs/2010.00316)
3. **Wavelength calibration, 2021.** An independent reduction compares joint
   ThAr/Fabry–Pérot and comb solutions and maps structured differences. It also
   explains why differential RV precision and wavelength accuracy for constants
   tests require different validation. [Paper](https://www.aanda.org/articles/aa/pdf/2021/02/aa39345-20.pdf)
4. **Fine-structure constant, 2022.** The comb-covered region was about
   485–700 nm, narrower than the full ESPRESSO range. The science case tests
   relative line positions in a quasar absorber rather than a stellar Doppler
   time series. [Paper](https://www.aanda.org/articles/aa/pdf/2022/02/aa42257-21.pdf)
5. **Epsilon Indi, 2024.** After nightly high-pass filtering, the high-cadence
   RV sequence had 0.30 m/s RMS against a mean 0.22 m/s photon uncertainty;
   stellar oscillations were the signal of interest. This does not establish
   long-period planet sensitivity. [Paper](https://www.aanda.org/articles/aa/full_html/2024/03/aa49197-24/aa49197-24.html)
6. **Iodine validation, 2025.** An absorption cell in the science beam supplies
   an external check on internal calibration and shows that injection geometry
   matters. [Paper](https://arxiv.org/abs/2504.18485)
7. **Current LFC status, 2026.** ESO records earlier background variability that
   affected line shapes, return to full operations in November 2025 and updated
   2026 manual guidance. Availability does not retroactively validate every
   earlier exposure. [ESO notices](https://www.eso.org/sci/facilities/paranal/instruments/espresso/news.html)

## Candidate project to discuss

A useful first project would be a calibration-consistency monitor, not another
single “precision score.” It would version exposures by DRS, observing mode,
calibrator state and injection configuration; produce detector-position residual
maps across calibration families; and report differential repeatability and
absolute accuracy separately. Complete nights and hardware states should be
held out, and injected Doppler shifts should be recovered before any correction
is used on science data.

This is a proposal for discussion, dependent on access to suitable calibration
and engineering products. It is not a completed pipeline or a statement of the
ESPRESSO team’s priorities. Machine-readable source notes are in
`data/espresso_papers.csv` and the project boundary is in
`data/instrument_dossiers.json`.
