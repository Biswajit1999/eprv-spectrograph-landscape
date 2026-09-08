# Completing the detailed instrument core

This chapter covers the nine detailed-core instruments that were not included in
the earlier reading notes. It follows 37 selected sources and distinguishes
instrument design, calibration tests, stellar measurements, science use and
dated status. It is not a claim to have reviewed every paper produced with each
instrument.

## SOPHIE

SOPHIE's first instrument description established its fibre-fed visible design.
The 2011 octagonal-fibre intervention then changed the illumination path: the
published stable-star repeatability improved from roughly 5–6 m/s to 1–2 m/s.
That comparison belongs to the samples and reduction used in the upgrade paper.
It does not make 1 m/s a universal label for every SOPHIE velocity.

The later ensemble zero-point method is scientifically useful but creates a
validation requirement: a target must not help estimate its own correction.
The 2024 ultraviolet comb experiment is a calibration result, not a stellar
time-series result. Finally, the 2026B call described conditional SOPHIE-RED
availability. A post-upgrade era needs a dated completion notice and new
characterization before historical performance can be transferred to it.

Sources: [instrument](https://ui.adsabs.harvard.edu/abs/2008SPIE.7014E..8BP/abstract),
[SOPHIE+](https://doi.org/10.1051/0004-6361/201219979),
[zero point](https://doi.org/10.1051/0004-6361/201525874),
[ultraviolet comb](https://www.nature.com/articles/s41467-024-51560-x),
[2026B status](https://programmes.insu.cnrs.fr/categorie-actualites/programmes-aa/).

## APF and the Levy spectrograph

The Automated Planet Finder combines robotic cadence with an iodine-cell Levy
spectrograph. First-light tests found sub-m/s RMS for two standards over three
months. A later 600-hour operations study reported a 1.35 m/s median internal
uncertainty across 4,954 velocities of 80 stars. These numbers have different
samples and definitions: neither is an instrument floor.

Automation is part of the measurement because scheduling shapes the spectral
window and sensitivity to aliases. A future replay could compare the actual
window with cadence-scrambled controls while tracking iodine templates and
reduction eras. The current Lick page establishes the facility, but the checked
page did not provide a dated operational statement; that gap remains visible.

Sources: [instrument](https://arxiv.org/abs/1402.6684),
[600-hour performance](https://arxiv.org/abs/1511.03664),
[operations thesis](https://escholarship.org/uc/item/8c32w845),
[official page](https://www.lickobservatory.org/explore/research-telescopes/automated-planet-finder/).

## iSHELL

iSHELL is a general 1.06–5.3 micrometre spectrograph with a specialist gas-cell
RV mode. The published analysis demonstrated about 5 m/s over roughly a year for
selected targets and about 3 m/s over a month for GJ 15 A. The current IRTF page
separately reports about 10 m/s for targets brighter than K=10 and 3–5 m/s for
very bright targets. These statements should not be collapsed into one value.

IRTF also records year-scale systematics, flat-field requirements caused by
fringing, and an approximate upper limit of 25 RV epochs per semester. Those
constraints motivate an order-by-order, flat-by-flat sensitivity study with an
explicit cadence window. The public archive can support selection, but it does
not provide one homogeneous RV product.

Sources: [instrument](https://ui.adsabs.harvard.edu/abs/2016SPIE.9908E..4SR/abstract),
[RV analysis](https://www.ipac.caltech.edu/publication/2019AJ....158..170C),
[archive](https://irsa.ipac.caltech.edu/docs/IRTF/IRSA_IRTF.html),
[2026B facility information](https://irtfweb.ifa.hawaii.edu/).

## Subaru IRD

IRD combines near-infrared spectra with simultaneous laser-comb information.
The forward model estimates segment-specific instrumental profiles and variable
telluric absorption. Simulations gave below-2 m/s precision for slowly rotating
mid-to-late M dwarfs at signal-to-noise above 100 per pixel. This is a conditional
simulation result, not a demonstrated multi-year floor.

The 2026 PyIRD preprint adds a software-era boundary. A controlled comparison
should reduce matched raw nights through legacy and current paths, then report
changes against water vapour, airmass and wavelength segment. The official IRD
page exists, but a dated 2026 availability statement was not identified in the
checked material.

Sources: [instrument](https://authors.library.caltech.edu/records/dke9a-dxz42),
[forward model](https://academic.oup.com/pasj/article/72/6/93/5903842),
[science use](https://academic.oup.com/mnras/article/530/3/3117/7651272),
[PyIRD preprint](https://arxiv.org/abs/2601.12669).

## PARVI

PARVI's commissioning paper reported roughly 4–10 m/s intra-night scatter for
HD 189733, distinct from its near-1 m/s design aim. A later hot-Jupiter recovery
is a science and commissioning result; a planet fit does not isolate long-term
instrument stability.

The current public record is structurally inconsistent. The historical JPL page
describes commissioning, and a March 2026 Palomar schedule confirms PARVI
hardware and calibrator use, while routine facility availability is not
established. The project therefore remains a status-conflict case rather than
being labelled simply operational or retired.

Sources: [project history](https://ao.jpl.nasa.gov/PARVI.html),
[pipeline and performance](https://doi.org/10.1117/1.JATIS.9.3.038006),
[commissioning science](https://www.ipac.caltech.edu/publication/2025JATIS..11a5001G),
[2026 schedule](https://reservations.palomar.caltech.edu/observing_schedule/run/6010/green_sheet/primary/).

## PARAS-2

PARAS-2 reported 2.65 m/s daily dispersion for 37 standard-star observations
over 35 days. The same study's 0.20–0.50 m/s inter-fibre drift was measured with
different light paths and cannot replace the stellar statistic. Current work on
the double scrambler, Cassegrain coupling module and detector cooling defines
new engineering eras.

A useful analysis would align stellar and calibration exposures with guiding,
temperature and fibre diagnostics, hold out complete nights, and test injected
signals. It should ask why the two light paths differ rather than advertising
the smaller number as achieved stellar precision.

Sources: [instrument](https://arxiv.org/abs/2401.07715),
[stellar sequence](https://www.aanda.org/articles/aa/pdf/2024/11/aa50934-24.pdf),
[Cassegrain module](https://arxiv.org/abs/2605.23532),
[institutional report](https://www.prl.res.in/~notices/websitedocs/2026/01/21/PRL-AR-2024-2025-ENG-reduced-21-01-2026-11-25-28.pdf).

## HARPS3

HARPS3's 0.10 m/s value is a design goal tied to a long, high-cadence survey.
ING's current material states that 2026B time is shared risk because commissioning
is incomplete and availability or performance is not promised. There is no
achieved stellar precision to report yet.

The appropriate current product is a requirement-to-acceptance table: calibration
tracking, stable-star RMS, cadence completeness and environmental exclusions
should be recorded separately. Seasonal claims must wait for a seasonal baseline.

Sources: [design](https://arxiv.org/abs/1608.04611),
[project](https://www.terrahunting.org/harps3.html),
[2026B call](https://www.ing.iac.es/astronomy/observing/ING_CfP_2026B.pdf),
[ING status](https://www.ing.iac.es/astronomy/instr.html).

## ANDES

ANDES is at preliminary design, not commissioning. The planned 0.4–1.8
micrometre simultaneous coverage, resolving power near 100,000 and precision
goals are requirements. The June 2026 consortium update states that documentation
entered the system preliminary design review process.

A transparent matrix can map each requirement to a subsystem, evidence class and
future acceptance test without predicting an outcome. Cross-arm calibration and
the complete science light path should remain distinct verification items.

Sources: [overview](https://arxiv.org/abs/2407.14601),
[RIZ design](https://arxiv.org/abs/2406.18317),
[calibration design](https://doi.org/10.1117/12.3104634),
[current milestone](https://andes.inaf.it/news/).

## G-CLEF

G-CLEF is also a planned instrument. Its 0.50 m/s requirement and 0.10 m/s goal
are not measurements. The design includes several resolution and fibre-feed
modes, so each mode needs its own light-path and stability definition.

The August 2026 blue-camera notice records a funding milestone for one subsystem,
not a completed spectrograph. A source-linked subsystem table can track enclosure,
fibres, calibration, detector and exposure meter while leaving unknown dates
unknown and reserving on-sky claims for future data.

Sources: [opto-mechanical design](https://gclef.cfa.harvard.edu/wp-content/uploads/2016/07/2014SPIE.91479A.pdf),
[project overview](https://ui.adsabs.harvard.edu/abs/2016SPIE.9908E..22S/abstract),
[technical page](https://www.gmt.iag.usp.br/index.php/en/projects/g-clef),
[blue-camera milestone](https://www.cfa.harvard.edu/news/giant-magellan-telescope-camera-reaches-fundraising-goal).

## Evidence boundary

The machine-readable evidence is stored in the nine matching `data/*_papers.csv`
tables and `data/instrument_dossiers.json`. No source plot, observatory logo or
substantial third-party text is bundled. Any later figure must be recreated from
cited numbers or independently processed public data and must state the sample,
timescale, instrument era and reduction version.
