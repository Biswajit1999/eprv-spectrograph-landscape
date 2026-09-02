# EPRV spectrographs: achievements, current state, and unresolved barriers

## Executive finding

The field has largely solved the problem of building environmentally
stabilized, fibre-fed spectrographs whose internal calibration can approach
or pass the 10 cm/s scale for limited experiments. It has not yet shown
routine, transferable 10 cm/s accuracy on ordinary Sun-like stars over the
years-long baselines required for an Earth analogue. The gap is not one
missing component. It is the interaction of stellar line-profile
variability, illumination, wavelength calibration, detector behaviour,
tellurics, barycentric timing, cadence, and pipeline provenance.

This distinction is central. EXPRES reported instrument-calibration
precision below 10 cm/s while explicitly excluding stellar photon noise;
NEID commissioning material reports sub-m/s quiet-star sequences; and
several instruments routinely support sub-m/s investigations. None of
those statements, by itself, is a demonstrated Earth-analogue detection
floor across targets and years.

## The technological progression

### HARPS and HARPS-N: stability as an architecture

HARPS established the modern pattern: a stationary bench, vacuum enclosure,
tight thermal control, fibre feed, simultaneous reference, and a reduction
pipeline designed together as a measurement system. HARPS-N transferred
that architecture to the northern sky and added a uniquely valuable solar
time series. Their enduring lesson is that calibration continuity matters
as much as short-term precision. HARPS's 2026 detector, electronics,
cooling, fibre, and pipeline upgrade creates a new instrumental era and a
velocity offset that must be modelled for programmes spanning the change.

### ESPRESSO: the VLT-scale optical system

ESPRESSO combines one or four VLT unit telescopes with a highly stabilized
spectrograph and multiple resolution modes. Its achievement is both
collecting area and metrology: broad optical coverage, a laser-frequency-
comb capable calibration chain, and a pipeline built for a more demanding
error budget than the first HARPS generation. The continuing scientific
challenge is that higher instrumental stability does not suppress stellar
convection, spots, faculae, or imperfect atmosphere/telescope coupling.

### EXPRES and NEID: error budgets made testable

EXPRES and NEID were designed around explicit subsystem allocations rather
than a single headline precision. EXPRES performance verification measured
effects from guiding, atmospheric dispersion, chromatic exposure timing,
fibres, modal noise, calibration sources, pixel-position non-uniformity,
and charge-transfer inefficiency. NEID's fibre-feed work demonstrates why
some illumination errors cannot be removed by a simultaneous wavelength
reference: calibration light and starlight do not necessarily illuminate
the optical system identically.

Their main community contribution is methodological. A claimed floor is
credible only when the experiment identifies which terms are present,
which were excluded, and whether the statistic is laboratory, solar,
short-term stellar, or long-baseline stellar performance.

### KPF: performance and maintainability are coupled

KPF extends stabilized optical Doppler work to Keck aperture. Its public
status history is unusually informative: detector noise, thermal events,
calibration availability, and a 2026 vacuum-pump failure are documented as
limitations on long-term RV interpretation. As of this report's status
date the instrument is offline. This is not evidence against the design;
it is evidence that maintainability, era boundaries, health telemetry, and
transparent quality flags belong inside an EPRV measurement model.

### CARMENES, HPF, SPIRou, and NIRPS: moving into the infrared

Cool stars emit more useful photons in the near infrared and produce larger
planetary RV amplitudes at a given planet mass and habitable-zone
insolation. The NIR also supplies chromatic leverage on activity. These
advantages motivated HPF, CARMENES's dual channels, SPIRou, and NIRPS.

The cost is a different systematic regime: dense and variable telluric
absorption, cryogenic optomechanics, infrared-detector persistence and
non-linearity, and stronger modal-noise concerns. SPIRou's simultaneous
spectropolarimetric capability is particularly relevant because it adds
direct magnetic information; NIRPS's simultaneous operation with HARPS
creates optical-to-NIR leverage for the same exposure. “Redder” is therefore
not simply “more precise”—it changes both the information and the errors.

### MAROON-X: target specialization

MAROON-X demonstrates the value of optimizing a stable optical instrument
for M-dwarf Doppler information rather than treating all stellar types as
the same measurement problem. Reported sub-m/s performance is important,
but remains conditional on target, cadence, wavelength weighting, and the
visiting-instrument operating model.

### HARPS3 and ANDES: the next experiments

HARPS3 couples a HARPS-family spectrograph to a robotic telescope and an
intensive nightly cadence. This tests a crucial idea: sampling and survey
operations can be as limiting as instantaneous instrument precision.
Delivery occurred in October 2025 and commissioning continues in 2026, so
its specifications remain goals.

ANDES combines ELT aperture with R~100,000 optical/NIR coverage. Its
baseline and goal wavelength-precision numbers are requirements, not
measurements. Its eventual contribution may be strongest where photon
collection currently dominates, but ELT complexity does not remove stellar
or atmospheric systematics.

## Nine barriers that remain

1. **Stellar variability** changes spectral line shapes rather than adding
   simple white velocity noise. Activity mitigation must generalize across
   stars and timescales.
2. **Photon information is target-dependent.** Resolution and wavelength
   span do not equal Doppler information without throughput and a spectrum.
3. **Calibration transfer is imperfect.** A comb can measure wavelength
   drift without seeing every illumination-dependent change experienced by
   starlight.
4. **Fibres are not complete scramblers.** Near/far-field changes and modal
   noise couple telescope conditions into the line-spread function.
5. **Thermomechanical stability has operational eras.** Maintenance,
   detector servicing, cryogenic events, and pressure changes create offsets.
6. **Detectors are part of the velocity model.** Pixel geometry, charge
   transfer, persistence, non-linearity, and read noise evolve.
7. **Tellurics are dynamic spectra.** Masking discards information; modelling
   introduces atmospheric and line-database uncertainty.
8. **Barycentric correction is chromatic.** Exposure timing, extinction, and
   guiding determine a wavelength-dependent effective midpoint.
9. **Pipelines define reported performance.** Templates, masks, extraction,
   outlier rejection, and version changes prevent naive archive rankings.

The committed `data/challenge_evidence.csv` makes these claims auditable.

## Community recommendations

- Publish the full definition and denominator behind every precision claim.
- Separate calibration residuals, instrumental repeatability, photon noise,
  stellar scatter, and planet-fit uncertainty.
- Version instrument eras and reduction pipelines in machine-readable data.
- Release solar and quiet-star benchmarks with raw quality flags and enough
  metadata for independent reduction.
- Compare pipelines on shared exposures, not instruments on heterogeneous
  archive planet samples.
- Treat negative commissioning findings and outages as reusable knowledge.
- Couple cadence experiments to stellar-activity inference rather than
  optimizing only visit counts.

## Conclusion

EPRV instrumentation has progressed from metre-per-second facility work to
sub-m/s on-sky investigations and, in constrained calibration experiments,
the 10 cm/s scale. The present frontier is measurement integrity across
years: a chain in which hardware stability, calibration transfer, detector
metrology, atmospheric correction, stellar physics, cadence, and software
provenance are jointly controlled. The strongest community resource is
therefore not a leaderboard. It is a dated, source-traceable map of what
each number actually measured.
