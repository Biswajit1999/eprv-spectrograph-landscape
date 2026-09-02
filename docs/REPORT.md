# Precision radial-velocity spectrographs: evidence and open problems

Status and sources checked **2 September 2026**. This is an independent
literature synthesis, not an observatory or consortium product.

## Summary

Stabilized spectrographs have made selected sub-metre-per-second measurements
and calibration tests at the ten-centimetre-per-second scale possible. The
literature does not support the stronger statement that 0.10 m/s accuracy is
routine across ordinary Sun-like stars and multi-year baselines. The remaining
gap is a coupled measurement problem involving the star, atmosphere, telescope,
fibre feed, calibration transfer, detector, cadence and reduction software.

The comparison contains 22 quantitative claims for 21 instruments. Nineteen
current or upcoming systems form the detailed performance core identified in
the 2026 *Annual Review of Astronomy and Astrophysics* review of precise radial
velocities. ANDES and G-CLEF are included only as planned systems. PARAS-2 adds
an operational southern instrument with a published 2024 stellar stability
test. No single-number ranking is calculated.

## How to read a precision number

Five quantities recur in the literature and are not interchangeable:

1. A **requirement or goal** is an engineering allocation before validation.
2. A **calibration residual** tests part of the instrument without a star.
3. An **internal uncertainty** estimates measurement noise under a model.
4. **Stellar or solar RMS** includes some combination of instrument, atmosphere,
   analysis and astrophysical variability.
5. A **planet-fit residual** also depends on the adopted astrophysical model.

The claim table records the metric, sample, baseline and caveat beside every
number. Figure 3 places unlike values on one axis only to expose their range and
contexts; it is not a performance leaderboard.

## Optical systems

### HARPS, HARPS-N and SOPHIE+

HARPS established the stationary, vacuum-enclosed, temperature-controlled,
fibre-fed architecture that shaped later facilities. An ESO commissioning
example reached about 1 m/s uncertainty in a one-minute exposure of a V=8 G6V
star. That is exposure-specific, not multi-year repeatability. The 2026 detector,
fibre, electronics, cooling and pipeline work defines a new instrument era.

HARPS-N provides a long, high-cadence solar record. The published three-year
analysis of 34,550 spectra reduced day-to-day scatter from 1.27 to 1.07 m/s after
wavelength-solution changes. SOPHIE's 2011 octagonal-fibre upgrade improved
reported standard-star repeatability from 5–6 to 1–2 m/s. Both cases show that
calibration software and illumination remain measurable error terms.

### APF-Levy, PFS, ESPRESSO, EXPRES and NEID

The Automated Planet Finder couples a dedicated telescope to the Levy
spectrograph. Its early survey reported a 1.35 m/s median internal uncertainty
from 4,954 measurements of 80 stars over 600 hours. PFS reported better than
1 m/s RMS on selected standards in its first five months, but later configuration
changes mean every value needs an instrument-era label.

ESPRESSO's instrument paper reported photon-noise uncertainties near 0.10 m/s
for M stars at very high signal-to-noise and 0.10–0.20 m/s for K/G dwarfs. These
are internal photon limits. EXPRES reported calibration precision below 0.10 m/s
while excluding photon noise and stellar variability; a separate 51 Peg analysis
reported 0.895 m/s residual RMS. Keeping both rows prevents a calibration number
from being promoted into a stellar claim.

NEID was designed around a 0.27 m/s single-visit instrumental requirement. Its
solar feed demonstrated 0.66 m/s RMS under good sky conditions and 0.41 m/s for
the best-condition subset over four commissioning months. WIYN now describes
NEID as commissioned and in full science operation.

### KPF and MAROON-X

KPF's public requirement is 0.50 m/s per visit with a 0.30 m/s goal. Those are
requirements, not long-term stellar RMS. Keck currently reports KPF offline
until further notice after an April 2026 vacuum-pump failure. Detector thermal
events and interventions create eras that must enter time-series analysis.

MAROON-X concentrates on late-type targets in the red optical. Its first two
years report regular sub-m/s on-sky work and a short-term instrumental floor
near 0.30 m/s. These results are conditional on selected targets and baselines.

## Near-infrared and dual-band systems

CARMENES observes with visible and near-infrared channels. A survey analysis
gives 1.6 m/s median internal precision at median S/N 95, or 0.8 m/s after
scaling to S/N 200. Scaling information content does not make stars equivalent.

HPF's Barnard's-star commissioning sequence was stable at about 1.5 m/s across
86 days. iSHELL uses a methane-isotopologue gas cell in K band; it demonstrated
5 m/s over about one year for Barnard's Star and 61 Cygni A, and 3 m/s over one
month for GJ 15 A. IRD forward
modelling achieved internal precision below 2 m/s for bright, slowly rotating
mid-to-late M dwarfs at S/N at least 100 per pixel.

SPIRou joins near-infrared velocimetry and spectropolarimetry. Standard stars
showed about 2 m/s RMS over weeks although photon uncertainty approached
0.5 m/s. NIRPS operates simultaneously with HARPS; first-light work reported
accuracy better than 1 m/s on a limited sample. PARVI commissioning observations
instead yielded 4–10 m/s intra-night stability against a roughly 1 m/s design
goal. The Caltech laboratory now lists PARVI as legacy; the gap between goal and
commissioning result remains useful evidence.

## PARAS-2 and planned systems

PARAS-2 is installed on the PRL 2.5-m telescope at Mount Abu. A 2024 study
reported 2.65 m/s daily dispersion from 37 standard-star observations over 35
days. Its 0.20–0.50 m/s inter-fibre drift was an off-sky uranium-argon test over
12 hours and is therefore not substituted for stellar performance.

HARPS3 was undergoing integration and commissioning in 2026, with shared-risk
open time advertised for 2026B. Its 0.10 m/s figure is a design goal. ANDES and
G-CLEF are future ELT/GMT instruments; their entries are engineering
requirements. None is represented as achieved stellar performance.

## Nine coupled barriers

1. **Stellar line-profile variability:** granulation, oscillations, spots and
   faculae are structured, wavelength-dependent signals.
2. **Photon information:** resolution and wavelength span matter only with
   throughput, the stellar spectrum, rotation and detector noise.
3. **Calibration transfer:** a reference measures drift but may not share the
   star's illumination path or line-spread function.
4. **Fibre illumination:** imperfect scrambling and modal noise couple guiding
   and seeing to the spectrum.
5. **Thermomechanical eras:** pressure, cryogenic cycles and replacement create
   offsets or new noise processes.
6. **Detector physics:** pixel geometry, charge transfer, persistence,
   non-linearity and read noise enter the velocity model.
7. **Telluric absorption:** masking loses information; modelling depends on
   atmospheric state and line databases.
8. **Chromatic barycentric timing:** extinction and guiding make the effective
   exposure midpoint wavelength dependent.
9. **Pipelines:** extraction, wavelength solutions, templates, masks and outlier
   policies affect published precision and must be versioned.

## Reporting standard and conclusion

Future claims should state the physical instrument and mode; hardware and
pipeline era; metric definition; target/sample; exposure and time-span
denominator; calibration source; uncertainty statistic; exclusions; primary
paper; dated status source; and what the number does not measure. Comparisons
should use shared exposures or a declared dataset, not unrelated archive planet
samples.

The field's achievement is not a single smallest number. It is the construction
of systems whose error terms can increasingly be tested. The outstanding task
is transferring that control to ordinary stars over years while retaining a
complete account of instrument, atmosphere, cadence and software state.
