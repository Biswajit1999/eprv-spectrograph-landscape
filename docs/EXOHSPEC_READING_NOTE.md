# EXOhSPEC reading note

This note follows seven selected design, laboratory, calibration and official
status sources. It does not claim a complete EXOhSPEC bibliography, a published
stellar radial-velocity result by this repository's author, or endorsement by
NARIT, the University of Hertfordshire, or ING.

## What the name refers to

EXOhSPEC has appeared in more than one physical setting. A compact University
of Hertfordshire prototype supported laboratory tests and an Isaac Newton
Telescope deployment. NARIT also describes an instrument developed for the
2.4-m Thai National Telescope. Results from one setting should not be silently
assigned to another.

## Reading path

### 2019 — folded optical design

The design study specified resolving power above 70,000 over 400–700 nm, a
short-term 3 m/s requirement, throughput above four percent and order
separation above 30 detector pixels. Its tolerancing, stray-light analysis and
prototype discussion are design evidence, not an achieved stellar-RV result.
[Source](https://uhra.herts.ac.uk/id/eprint/14227/)

### 2021 — actively controlled laboratory prototype

Jones et al. described a compact, off-the-shelf prototype with a bifurcated
fibre, simultaneous thorium-argon reference and piezoelectric active control.
In a standard laboratory it reached resolving power above 70,000 and a measured
motion of 3.5 millipixels, interpreted by the authors as approximately 4 m/s.
That is a laboratory displacement test, not repeatability on stellar spectra.
[Source](https://arxiv.org/abs/2011.10526)

### 2024 — fibre modal-noise experiment

The galvanometer-agitation experiment compared multimode fibres using the
Hertfordshire prototype. The best reported GI50t result reduced the study's
modal-noise metric by about 60 percent while losing about five percent of output
light. The result is conditional on the fibre and laboratory setup; it does not
yet quantify the effect on a long stellar RV time series.
[Source](https://academic.oup.com/rasti/article/3/1/8/7505148)

### 2025 — fused-silica metalon calibration

The metalon study tested two cavity spacings against thorium-argon. The active
enclosure held 0.8 mK stability. TERRA and SERVAL both measured 8 m/s temporal
drift for the metalon over 470–780 nm; polynomial flattening reduced that result
to 5 m/s. The paper states that spectrograph active stabilization was not
engaged and that the result did not meet the 1 m/s calibration requirement.
Long-term behaviour remains open.
[Source](https://academic.oup.com/rasti/article/doi/10.1093/rasti/rzaf036/8230991)

## Current status cannot yet be stated as one settled label

Two current NARIT pages disagree. The English technology page says EXOhSPEC has
been installed and tested with the 2.4-m national telescope. The Thai National
Observatory roster labels it “under development.” Neither checked page provides
a dated commissioning report or an achieved stellar-RV time series that resolves
the difference. The directory therefore retains `status_conflict`.

- [NARIT technology page](https://www.narit.or.th/en/technology-development/advanced-optics/EXOhSPEC)
- [Thai National Observatory roster](https://narit.or.th/th/observatory/thai-national-observatory)

ING separately records first light for its EXOhSPEC deployment in June 2021 and
decommissioning on 27 May 2024. That history should not be used to infer the
current state of the Thai instrument.
[ING record](https://www.ing.iac.es/PR/inst.php?inst=EXOhSPEC&tel=int)

## What is established, and what is not

Established in the selected sources:

- a compact high-resolution optical design and laboratory prototype;
- active image-motion control at an approximately 4 m/s laboratory scale;
- quantified modal-noise and throughput trade-offs for one fibre experiment;
- a thermally controlled metalon experiment with measured 8 m/s temporal drift;
- evidence of an earlier ING deployment and conflicting NARIT status statements.

Not established by the selected sources:

- a completed, peer-reviewed on-sky stellar RV performance characterization for
  the Thai National Telescope instrument;
- long-term stability across nights, seasons or maintenance states;
- a demonstrated 3 m/s or 1 m/s stellar time-series result;
- one unambiguous current operational status.

## Future analysis question

Can a reproducible verification notebook use released laboratory data to repeat
the image-motion, modal-noise and calibration-drift tests, while defining the
additional observations and metadata required before any stellar precision
claim? A useful first version would preserve raw measurement units, keep each
physical setup separate, reproduce reported summary values, and mark any missing
data rather than filling them by assumption. This is a future analysis question,
not completed research, a publication claim, or an endorsed instrument programme.
