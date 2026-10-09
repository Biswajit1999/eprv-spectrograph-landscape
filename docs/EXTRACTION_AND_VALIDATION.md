# From pixels to radial velocity: extraction and validation

An environmentally stable spectrograph does not directly output a planet-ready
radial velocity. The reported value also depends on extraction, wavelength
calibration, the reference-frame correction, the stellar template or mask,
detector behaviour, atmospheric treatment and quality-control decisions. This
note defines those layers without implying that one pipeline family is always
superior.

## Cross-correlation functions

A cross-correlation-function (CCF) pipeline shifts a weighted numerical line
mask across the observed spectrum and combines the selected lines into an
average profile. A fitted CCF centroid provides the velocity, while its width,
contrast and asymmetry can act as diagnostics. The compression is efficient and
interpretable, but the line mask, order weights, rejected wavelengths and
profile model are part of the measurement definition.

Primary example: Baranne et al. (1996), [ELODIE: A spectrograph for accurate
radial velocity measurements](https://doi.org/10.1051/aas:1996251).

## Empirical templates and forward models

Template-matching methods build a high-signal stellar template from repeated
observations and fit the shift of each observation, often order by order. This
retains pixel-level information that a single average CCF profile compresses,
but it also makes template construction, interpolation, continuum treatment,
telluric rejection and outlier policy explicit sources of model dependence.
Broader forward models may additionally fit the line-spread function,
wavelength solution, gas-cell or simultaneous-calibration spectrum and
atmospheric absorption.

Primary examples:

- Zechmeister et al. (2018), [SERVAL: SpEctrum Radial Velocity
  AnaLyser](https://doi.org/10.1051/0004-6361/201731483).
- Butler et al. (1996), [Attaining Doppler Precision of 3 m/s](https://doi.org/10.1086/133755).
- Petersburg et al. (2020), [An Extreme Precision Radial Velocity Pipeline:
  First Radial Velocities from EXPRES](https://arxiv.org/abs/2003.08851).

## Barycentric correction and exposure weighting

Earth's orbital and rotational motion is much larger than the signals sought.
The transformation to the Solar System barycentric frame is relativistic rather
than a simple subtraction. At centimetre-per-second scales, telescope position,
stellar astrometry, timing and chromatic flux variations matter. The correct
exposure-level operation uses the photon history to weight the barycentric
correction; evaluating one value at the shutter midpoint can create a systematic
error.

Primary examples:

- Wright & Eastman (2014), [Barycentric Corrections at 1 cm/s for Precise
  Doppler Velocities](https://doi.org/10.1086/678541).
- Tronsgaard et al. (2019), [Photon-weighted barycentric correction and its
  importance for precise radial velocities](https://doi.org/10.1093/mnras/stz2181).

## Detector and atmospheric systematics

Detectors are not perfect, continuous wavelength rulers. Pixel block stitching,
intrapixel response, charge-transfer inefficiency, persistence, non-linearity
and read noise can create structured velocity errors. Telluric lines are also
time-variable and can blend with stellar lines as the barycentric velocity
changes. A simultaneous calibrator does not automatically correct an effect
that follows a different optical path or interacts differently with the detector
and reduction model.

Primary example: Dumusque et al. (2015), [Characterization of a spurious
one-year signal in HARPS data](https://doi.org/10.1088/0004-637X/808/2/171).

## Sun-as-a-star feeds

Small solar telescopes can inject disk-integrated sunlight into the same
spectrograph and pipeline used for night-time stellar observations. Their high
cadence makes instrument and pipeline changes visible, while spatially resolved
solar observations provide external context for line-profile variability.
These series do not remove astrophysics: their RMS still includes solar
oscillations, granulation, magnetic activity, weather, observing cadence,
calibration and pipeline choices. A solar result is therefore an end-to-end
validation in a named context, not a universal instrumental floor.

Primary examples:

- Collier Cameron et al. (2019), [Three years of Sun-as-a-star radial-velocity
  observations on the approach to solar minimum](https://doi.org/10.1093/mnras/stz1215).
- Lin et al. (2022), [Observing the Sun as a star: design and early results from
  the NEID solar feed](https://arxiv.org/abs/2112.05711).

## Reporting boundary

Pipeline comparisons should use the same raw exposures or a clearly declared
shared dataset. A lower RMS from different targets, epochs or activity states is
not evidence that one extraction method is intrinsically superior. Every public
number should retain the pipeline version, calibration version, mask or template,
target/sample, time baseline, statistic and exclusions needed to interpret it.
