# Seven-instrument reading wave

This chapter records selected reading paths for KPF, MAROON-X, CARMENES, HPF,
SPIRou, NIRPS and the Magellan Planet Finder Spectrograph. Each section separates
design values, subsystem tests, stellar measurements, current status and future
analysis. It is not a claim to have read every science paper using an instrument.

## KPF

KPF's design requirement of 0.50 m/s per observation and 0.30 m/s goal are not
stellar performance results. The as-built paper describes the 445–870 nm,
R approximately 98,000 system, its Ca II H and K channel, exposure meter, solar
feed and comb/etalon calibration. The SoCal paper supplies an empirical check:
high-cadence KPF and NEID solar velocities agreed at 0.30–0.40 m/s over
several-hour intervals, while those data also exposed early detector and
wavelength-calibration problems.

The current boundary is operational rather than statistical. Keck states that
KPF is offline until further notice after an April 2026 turbo-pump failure.
The actively developed pipeline records service missions, KPF eras, master-file
changes and recent order-trace fixes. A later analysis should replay public solar
products by complete instrument era, then start a separate post-repair validation
when a dated return notice and new observations exist.

- [Preliminary design](https://authors.library.caltech.edu/records/c0hv1-hks70)
- [SoCal paper](https://arxiv.org/abs/2311.05129)
- [As-built system](https://authors.library.caltech.edu/records/gn5gn-t9r95)
- [Pipeline releases](https://github.com/Keck-DataReductionPipelines/KPF-Pipeline/releases)
- [Current Keck status](https://www2.keck.hawaii.edu/realpublic/observing/public_instrument_info/kpf/status/)

## MAROON-X

The early sources document laboratory development and a changing deployment
plan. Commissioning occurred at Gemini North, and the first-two-years report
describes regular sub-m/s on-sky results with a short-term instrumental floor
near 0.30 m/s. The 2025 ensemble study measured an etalon drift around
0.022 m/s/day and calibrated observing-run offsets to about 0.5 m/s. Applied to
HD 3651, the reported residual RMS was below 0.70 m/s in both channels over
29 months.

Gemini separately reports two 2024A echelle-image shifts, caused by an earthquake
and a power loss, and warns that velocities from the existing reduction were
uncertain near 20 m/s. A replay should leave out entire stars and runs, preserve
separate red and blue channels, and treat 2024A as an incident-recovery era.

- [Development](https://arxiv.org/abs/1606.07140)
- [Gemini design update](https://arxiv.org/abs/1805.09276)
- [Commissioning](https://arxiv.org/abs/2106.02157)
- [First two years](https://arxiv.org/abs/2210.06563)
- [Gemini incident notice](https://www.gemini.edu/news/instrument-announcements)
- [Ensemble drift analysis](https://arxiv.org/abs/2502.15074)

## CARMENES

CARMENES records visible and near-infrared spectra simultaneously, but the
channels do not carry equal velocity information. The 2018 information study
found that 700–900 nm generally carries the strongest Doppler information for
M dwarfs, with longer wavelengths becoming competitive mainly for M8–M9 stars.
SERVAL adds template velocities, chromatic index and line-width diagnostics.

DR1 contains 19,633 spectra for 362 targets and 18,642 high-level RVs for 345
targets. Its median internal uncertainty of 1.27 m/s is not a median stellar RMS.
Nightly zero points are estimated from quiet stars with the target excluded;
where a direct value cannot be calculated, adjacent-night estimates are used.
The 2024 study reports 1.6 m/s median internal precision at median signal-to-noise
95 and a scaled 0.8 m/s at signal-to-noise 200. The scaled value is a controlled
comparison, not a second achieved survey precision.

- [Instrument report](https://carmenes.caha.es/ext/conferences/CARMENES_SPIE2016_Quirrenbach.pdf)
- [SERVAL](https://www.aanda.org/articles/aa/abs/2018/01/aa31483-17/aa31483-17.html)
- [Wavelength information](https://www.aanda.org/articles/aa/abs/2018/04/aa32054-17/aa32054-17.html)
- [Chromatic activity](https://www.aanda.org/articles/aa/full_html/2020/09/aa38213-20/aa38213-20.html)
- [DR1](https://www.aanda.org/articles/aa/pdf/2023/02/aa44879-22.pdf)
- [Precision study](https://www.aanda.org/articles/aa/pdf/2024/12/aa50836-24.pdf)
- [Current call](https://www.caha.es/APPS/CfP/public/)

## HPF

HPF's conceptual and calibration papers describe a cryogenic near-infrared
instrument, dual fibres and comb/etalon/lamp references. A laboratory
environmental test reached 0.6 mK RMS over 15 days; that is thermal stability,
not a stellar velocity. The comb paper reported 1.53 m/s differential RMS for
Barnard's Star over months while simultaneous-fibre calibration tests reached
about 0.06 m/s. These two numbers remain separate.

The six-month etalon study followed roughly 3,500 resonant modes. Average drift
was about 0.02 m/s/day, with local chromatic departures up to plus or minus
0.05 m/s/day. It supported calibration below 0.10 m/s over a night and below
0.30 m/s over roughly ten days, but also showed why one scalar drift is
insufficient. A later notebook should compare scalar, order-wise and smooth
chromatic corrections on held-out dates, stratified by HET pupil geometry.

- [Conceptual design](https://arxiv.org/abs/1209.1686)
- [Calibration system](https://arxiv.org/abs/1408.3632)
- [Environmental control](https://arxiv.org/abs/1610.06216)
- [Comb and stellar spectroscopy](https://tf.nist.gov/general/pdf/2985.pdf)
- [Etalon drift](https://arxiv.org/abs/2103.08456)
- [Far-field scrambling](https://arxiv.org/abs/2103.05148)
- [Commissioning note](https://hpf.psu.edu/2019/02/19/hpf-commissioning/)

## SPIRou

SPIRou combines 0.95–2.50 micrometre spectroscopy and polarimetry at resolving
power 70,000 plus or minus 3,000. The instrument paper measures distinct regimes:
a 0.07 m/s relative calibration-channel RMS over 32 hours, 3.4 m/s on one
six-hour stellar run, and roughly 2 m/s over weeks for mid-M dwarfs. None can
replace another. The paper also flags detector persistence on faint targets,
crosstalk from simultaneous calibration and continued telluric-correction work.

Later science shows why different line masks matter for magnetic activity.
A sensitivity table should condition velocity changes on water vapour, airmass,
prior-exposure brightness and magnetic sensitivity while reporting the Doppler
information lost by each telluric mask.

- [Input catalogue](https://academic.oup.com/mnras/article/475/2/1960/4768264)
- [Instrument performance](https://academic.oup.com/mnras/article/498/4/5684/5897365)
- [Telluric and stellar modelling](https://academic.oup.com/mnras/article/511/2/1893/6468761)
- [Multi-season activity application](https://academic.oup.com/mnras/article/535/4/3363/7887819)
- [CFHT observer cookbook](https://www.cfht.hawaii.edu/Instruments/SPIRou/SPIRou_cookbook.php)

## NIRPS

NIRPS uses adaptive-optics-assisted injection and separate high-accuracy and
high-efficiency fibre modes. Early science reports better-than-1 m/s accuracy
for selected stars, but the result belongs to its commissioning sample and
reduction. ESO now offers the instrument and has released pipeline-reduced
spectra from operations beginning in April 2023.

A September 2026 preprint proposes night-sky emission corrections constructed
separately for the two modes. Its recency and preprint status remain visible.
A replay should hold out complete nights and wavelength blocks, measure bias
together with false-signal creation, and use simultaneous HARPS data only after
matching timestamps and stellar models.

- [Front end](https://arxiv.org/abs/2207.14143)
- [First light](https://arxiv.org/abs/2406.08304)
- [Instrument characterization](https://arxiv.org/abs/2507.21767)
- [Archive release](https://www.eso.org/cms/eso-archive-news/release-of-nirps-pipeline-reduced-spectra.html)
- [Current ESO offering](https://www.eso.org/sci/facilities/lpo/cfp/cfp118/instruments.html)
- [Sky-correction preprint](https://arxiv.org/abs/2609.03374)

## Magellan PFS

PFS is an iodine-cell spectrograph on Magellan Clay. Its commissioning report
states below-1 m/s RMS for selected standards over the first five months. Later
configuration changes and long-baseline science mean that result cannot be
assigned to every PFS velocity. A five-year PFS sequence contributed to the
HD 133131 system analysis, but a multi-planet or multi-instrument fit is not an
instrument-only stability test.

Current Carnegie and Las Campanas pages list PFS. The broad institutional
statement of better-than-1 m/s precision does not specify sample, cadence,
pipeline or hardware era. A later analysis first needs a dated configuration
and template ledger; unresolved velocities should remain unassigned rather than
being forced into one era.

- [Construction report](https://users.obs.carnegiescience.edu/crane/pfs/docs/pfs-spie2008.pdf)
- [Commissioning](https://carnegiescience.edu/carnegie-planet-finder-spectrograph-integration-and-commissioning)
- [Long-baseline application](https://arxiv.org/abs/1608.06216)
- [VELOCE DR1 use](https://www.aanda.org/articles/aa/abs/2024/06/aa48400-23/aa48400-23.html)
- [Carnegie roster](https://carnegiescience.edu/our-research/instrumentation/planetary-science-instrumentation)
- [Las Campanas documentation](https://www.lco.cl/technical-documentation/)

## Evidence boundary

The machine-readable records are the seven matching paper tables in the data
directory and their entries in the dossier JSON. No third-party plot or
instrument image is copied. Future figures must be generated from cited numeric
tables or independently processed public data, with measurement definitions and
instrument eras carried into the caption.
