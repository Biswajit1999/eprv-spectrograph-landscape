# Survey, legacy, and general-purpose instrument notes

This chapter adds 44 selected sources for ten instruments. It is a reading map,
not a ranking and not a complete bibliography. A number remains attached to the
target, duration, observing mode, reduction, and evidence type that produced it.

## HERMES — large-sample radial velocities

HERMES was built for multiplexed Galactic archaeology. Its four-channel,
roughly 400-fibre design and resolving power near 28,000 serve a different
measurement problem from a single-object stabilized Doppler spectrograph. The
GALAH reduction paper reports fibre cross-talk below about 0.5 percent and
wavelength-solution accuracy better than 1 km/s. The DR2 velocity paper reports
typical accuracy of 0.1 km/s for 336,215 stars, while the later GALAH+ work finds
generally similar uncertainties and external median differences below 30 m/s for
most comparison groups. Those are survey-catalogue results, not evidence for a
metre-per-second instrument floor.

The useful analysis question is therefore fibre- and population-aware: which
repeat-visit residuals follow fibre, observing run, template group, or stellar
variability? The source ledger is `data/hermes_papers.csv`.

## UCLES — historical iodine velocities

The UCLES record connects the iodine forward-modelling method to a long-running
southern planet search. The cell was inserted behind the slit, placing its lines
in the stellar beam, but star templates, slit illumination, detector state, and
reduction version still define distinct eras. The official AAT material now
places UCLES under decommissioned instruments without giving a precise retirement
date on the reviewed page. A future archive analysis should reconstruct those
eras before testing signals whose periods cross them. See `data/ucles_papers.csv`.

## ESPaDOnS — drift in a spectropolarimetric system

ESPaDOnS covers a broad optical-to-near-infrared range and produces intensity,
polarization, diagnostic, and uncertainty products. A young-star application
reported run residuals of about 10 and 15 m/s, but those residuals also depend on
stellar-activity modelling. CFHT's Libre-ESpRIT documentation describes optimal
extraction, wavelength calibration, telluric drift correction, and approximately
190,000 samples at 1.8 km/s sampling. It also states what the package does not do,
including exposure co-addition and downstream line analysis. Sampling and
calibration-fit residuals must not be relabelled as stellar RV precision. See
`data/espadons_papers.csv`.

## TRES — reconnaissance and multi-order checks

TRES is a fibre-fed, resolving-power approximately 44,000 instrument widely used
for transit-candidate reconnaissance, stellar classification, and relative
velocities. Its public follow-up products span heterogeneous targets, rotations,
signal-to-noise ratios, and visit counts. That diversity makes a single precision
label unhelpful. A controlled analysis should hold out complete targets and ask
which orders and stellar classes dominate repeat-visit residuals. See
`data/tres_papers.csv`.

## IGRINS — telluric forward modelling in H and K

IGRINS simultaneously covers the H and K windows at resolving power near 45,000.
The public IGRINS RV pipeline constructs nightly telluric templates and models the
instrumental resolution. Its validation reports 31.1 m/s in H and 26.8 m/s in K
for narrow-line standards. The workflow requires sufficiently good starting
velocity and rotation values and may require repeated convergence and uncertainty
runs. These band-, target-, and version-specific measurements should not be
generalized. Gemini's current tools refer to IGRINS-2, so the physical identity
and deployment of original IGRINS remain an explicit census question. See
`data/igrins_papers.csv`.

## CORALIE — simultaneous reference over 25 years

CORALIE uses two fibres, double scrambling, a controlled enclosure, and a
simultaneous thorium reference. Its long-running southern survey now spans about
25 years and 1,647 main-sequence stars in the selected catalogue paper. That
baseline supports long-period work but also crosses hardware generations,
cross-correlation masks, and zero points. The next archive study should attach a
generation identifier to every velocity and test long-period signal preservation
across boundaries. See `data/coralie_papers.csv`.

## FEROS — broad coverage rather than dedicated EPRV design

FEROS covers roughly 350–920 nm at resolving power near 48,000. An early Tau Ceti
sequence reported 8.3 m/s RMS over 245 days, while ESO's instrument overview says
FEROS was not intended as an RV machine and gives about 25 m/s or better as a
general Object-Calibration capability. These statements are compatible because
they describe different evidence and scope. Reproducing the early sequence with
modern and historical reductions across more standards would test transfer. See
`data/feros_papers.csv`.

## FIDEOS — a bounded commissioning result

FIDEOS combines an octagonal fibre, thermal control, and simultaneous calibration
over approximately 420–800 nm at resolving power near 43,000. The commissioning
paper and ESO summary report about 8 m/s stability over several consecutive
nights. That result is kept as a short-baseline measurement; it does not establish
seasonal performance or current availability. See `data/fideos_papers.csv`.

## PEPSI — configuration is part of the measurement

PEPSI offers resolving powers near 43,000, 120,000, and 270,000, six
cross-dispersers, several feeds, polarimetric paths, and Fabry-Perot capability.
Its solar atlases test line shape and spectral quality but do not measure the
night-time LBT stellar light path. A useful comparison must preserve mode,
cross-disperser, feed, and polarization state rather than combining all PEPSI
data under one performance value. See `data/pepsi_papers.csv`.

## Subaru HDS — iodine, detector response, and setup state

HDS is a configurable slit spectrograph with iodine coverage from about 500 to
650 nm and image slicers spanning resolving powers near 80,000–165,000. Official
documentation reports signal-dependent detector nonlinearity that differs between
the two CCD chips. The current page also records degraded reflectivity in both
image rotators as of July 2026, while the flux-weighted light monitor is currently
unavailable. These are distinct detector, throughput, illumination, and timing
terms; none should be converted directly into an RV offset without data. See
`data/hds_papers.csv`.

## Common analysis discipline

Across this wave, the main rule is to preserve measurement context. Survey
accuracy, calibration-fit residuals, short commissioning sequences, planet-fit
residuals, spectral resolution, and public capability statements are different
quantities. Each proposed analysis in `data/instrument_dossiers.json` therefore
uses held-out nights, targets, fibres, or configurations and is labelled as work
not yet completed.
