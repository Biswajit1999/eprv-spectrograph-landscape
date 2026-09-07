# How precision radial-velocity measurements work

This chapter is a starting point for readers who have not reduced a stellar
spectrum. It explains the measurement chain before the instrument directory.
It deliberately separates a spectrograph, a radial-velocity measurement and a
planet interpretation: those are related, but they are not the same thing.

## 1. What a spectrograph records

A telescope collects light; a spectrograph separates that light by wavelength.
In a high-resolution echelle spectrograph, a diffraction grating disperses the
light into many overlapping spectral orders and a cross-disperser separates
those orders on a two-dimensional detector. The output is not a ready-made
velocity. It is detector counts whose coordinates, background, blaze response,
bad pixels and line-spread function must be modelled.

Stellar atmospheres absorb light at characteristic wavelengths. These
absorption lines supply Doppler information because a line-of-sight velocity
changes their observed wavelengths. For speeds much smaller than the speed of
light,

`Delta lambda / lambda approximately equals v_r / c`.

The sign convention must be stated: positive radial velocity normally means
recession. Real pipelines use a relativistic Doppler convention where needed;
the small-shift expression is an explanation, not a complete reduction formula.

Resolving power is

`R = lambda / delta lambda`.

It describes how finely the instrument separates wavelengths. It is not an RV
accuracy. A spectrum with resolving power 100,000 has a resolution-element
velocity scale near 3 km/s, yet a model can locate the collective shift of many
well-sampled lines far more precisely than one resolution element. That
statistical precision does not remove calibration, atmospheric or stellar
systematics.

## 2. Why more photons and sharper lines help

Bouchy, Pepe and Queloz (2001) express the photon-limited uncertainty as

`sigma_v = c / (Q sqrt(N_e))`,

where `N_e` is the detected photoelectron count and `Q` describes the Doppler
information in the recorded spectrum. Deep, narrow lines with steep slopes
carry more shift information than a nearly flat continuum. Spectral type,
rotational broadening, wavelength coverage, resolving power, sampling and
throughput therefore matter together.

This formula is a statistical lower bound under its assumptions. It is not a
prediction of multi-year stellar RMS and should never be compared directly with
a planet-fit residual without explaining the different contexts.

## 3. Three ways to attach a wavelength reference

### Absorption cell

An iodine cell places a dense reference spectrum in the same beam as the star.
Butler et al. (1996) modelled each observed segment as a stellar template times
an iodine transmission spectrum, convolved with the instrumental profile. The
wavelength scale, profile and stellar shift are solved for each exposure. The
shared path is valuable, but the iodine and stellar spectra must be disentangled
and the useful iodine band does not cover the entire optical spectrum.

### Simultaneous reference fibre

HARPS illustrates another architecture. One fibre carries the star and a second
can carry a ThAr or Fabry-Perot reference during the exposure. The calibrator
tracks spectrograph drift, but it does not traverse exactly the same atmospheric,
telescope and fibre path as the stellar photons. Illumination transfer remains
part of the error budget.

### Calibration sources are complementary

A hollow-cathode lamp supplies atomic lines with laboratory wavelength
information. A Fabry-Perot etalon supplies a dense, regular comb useful for a
local relative solution, but its absolute scale must be anchored. A laser
frequency comb can supply accurately spaced, frequency-referenced modes, but
spectral coverage, mode filtering, injection and operational reliability still
matter. ESO's ESPRESSO quality-control description explicitly uses ThAr,
Fabry-Perot and laser-comb frames for different roles. Schmidt et al. (2026)
showed that a precise calibrator does not by itself remove fibre-injection
effects.

## 4. Turning spectra into relative velocities

A cross-correlation-function pipeline slides a weighted line mask across the
spectrum and finds the shift that maximizes the match. A fitted mean profile can
also provide line width, contrast and bisector diagnostics. It is efficient and
has a long operational history, but the result depends on the mask, line weights,
excluded wavelength regions and profile model.

Template matching constructs a high-signal stellar template and fits individual
observations against it. It can use more pixel-level information and avoids a
fixed binary mask, but template construction, interpolation, continuum handling,
outlier rejection and telluric treatment still influence the answer. Neither
method automatically distinguishes a moving stellar spectrum from changing
line shapes.

## 5. Correcting the observer's motion

The observatory is moving because Earth rotates and orbits, and the Solar System
itself has a defined barycentric reference frame. Wright and Eastman (2014)
describe the relativistic barycentric correction needed for centimetre-per-second
work and the sensitivity to timing, observatory position and stellar astrometry.

An exposure has duration, not a single physical instant. Clouds and changing
airmass can make the photon-weighted midpoint wavelength dependent. Tronsgaard
et al. (2019) found that using only a geometric midpoint can produce a typical
second-order error around 0.1 m/s and exceed 1 m/s in realistic cases. An
exposure meter records when the useful photons arrived; its time and colour
information should be retained.

## 6. Why a repeating shift is not automatically a planet

A planet and star orbit their common centre of mass. The radial-velocity
semi-amplitude depends on orbital period, planet mass, stellar mass, inclination
and eccentricity. Without an independent inclination, the usual observable is
minimum mass, `M sin(i)`.

Other processes also perturb line positions or shapes:

- acoustic oscillations and granulation act over minutes to hours;
- spots, faculae and suppressed convective blueshift rotate across the disc;
- magnetic cycles create longer changes;
- Earth's atmospheric absorption moves relative to stellar lines as the
  barycentric velocity changes;
- detector, calibration, fibre and maintenance changes can introduce eras.

Dumusque et al. (2011) used HARPS observations and simulations to examine
cadences that average short-timescale stellar noise. Cunha et al. (2014) showed
that weak telluric lines can already affect precise optical RVs and that the
effect depends on atmospheric conditions and barycentric velocity. The RV
fitting challenge (Dumusque et al. 2017) showed why recovery methods must be
tested against mixtures of planets, stellar processes and instrumental noise.

## 7. A spectrograph taxonomy

“Spectrograph” is a broad hardware class, not a performance label.

| Class | Examples | Measurement emphasis | In this census? |
|---|---|---|---|
| Dedicated precision-RV | HARPS, ESPRESSO, EXPRES, NEID | Repeated high-resolution stellar Doppler measurements with controlled illumination and stability | Yes |
| General high-resolution with RV evidence | UVES, Subaru HDS, several HRS instruments | Broad spectroscopy programme that includes some RV studies | Yes, in a separate inclusion tier |
| Survey RV spectrograph | Gaia RVS | Large stellar survey; R about 11,500 over 845–872 nm | No; shown as a comparator |
| General-purpose space spectrograph | JWST NIRSpec | Galaxies, stellar populations and exoplanet atmospheres at R about 100–2,700 | No; shown as a comparator |

JWST/NIRSpec is not “missing” from an EPRV census. It is a spectrograph built for
different questions. Gaia RVS does measure radial velocity in space, but its
resolution, survey strategy and km/s-scale performance regime differ from the
ground-based exoplanet precision-RV systems discussed here.

## 8. Vocabulary that prevents false comparisons

- **Design goal:** an engineering target, not an achieved observation.
- **Calibration residual:** agreement within part of the wavelength solution.
- **Internal uncertainty:** a model-based statistical error for one observation.
- **Stellar or solar RMS:** scatter containing a context-specific mixture of
  instrument, atmosphere, reduction and astrophysics.
- **Planet-fit residual:** scatter remaining after an adopted astrophysical
  model; it is conditional on that model.
- **Accuracy:** closeness to a physically correct value.
- **Precision:** repeatability or statistical concentration. A precise result
  can still contain a common bias.

## Primary sources used in this chapter

1. Bouchy, Pepe & Queloz (2001), [Fundamental photon noise limit to radial velocity measurements](https://doi.org/10.1051/0004-6361:20010730).
2. Butler et al. (1996), [Attaining Doppler Precision of 3 m/s](https://doi.org/10.1086/133755).
3. Wright & Eastman (2014), [Barycentric Corrections at 1 cm/s for precise Doppler velocities](https://arxiv.org/abs/1409.4774).
4. Tronsgaard et al. (2019), [Photon-weighted barycentric correction](https://arxiv.org/abs/1908.00991).
5. Dumusque et al. (2011), [Observational strategies to reduce stellar oscillation and granulation effects](https://doi.org/10.1051/0004-6361/201014097).
6. Dumusque et al. (2017), [Radial-Velocity Fitting Challenge I](https://arxiv.org/abs/1607.06487) and [II](https://arxiv.org/abs/1609.03674).
7. Dumusque (2018), [Measuring precise radial velocities on individual spectral lines I](https://arxiv.org/abs/1809.01548).
8. Cunha et al. (2014), [Impact of micro-telluric lines on precise radial velocities](https://doi.org/10.1051/0004-6361/201423723).
9. Rajpaul et al. (2020), [A robust, template-free approach to precise radial velocity extraction](https://doi.org/10.1093/mnras/staa173).
10. NASA Exoplanet Archive, [Predicted observables for exoplanets](https://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html).
11. ESO, [HARPS science modes](https://www.eso.org/sci/facilities/lasilla/instruments/harps/inst/scimodes.html) and [ESPRESSO wavelength calibration QC](https://www.eso.org/observing/dfo/quality/ESPRESSO/qc/waveLFC_qc1.html).
12. ESA Gaia, [RVS science performance](https://www.cosmos.esa.int/web/gaia/science-performance).
13. STScI, [JWST NIRSpec documentation](https://jwst-docs.stsci.edu/jwst-near-infrared-spectrograph).

All web pages were checked on 7 September 2026. Numerical statements retain
their measurement context; none is used as a cross-instrument ranking.
