# Final census reading notes

This chapter completes the selected-source path for every physical instrument in
the 53-record directory. It adds 44 records across twelve evidence tables and
fifteen instrument dossiers. “Complete” refers to dossier coverage of this
declared census, not to every publication that has ever used these instruments.

## Dedicated and survey Doppler instruments

- **BOES:** its three fibre diameters imply resolving powers near 90,000,
  45,000 and 30,000. KASI's sub-5 m/s iodine statement lacks a sample and
  baseline, so it is not assigned to every BOES observation.
- **CAFE:** the CAFE2 paper separates roughly 3 m/s ThAr stability from an
  approximately 8 m/s one-night stellar result at S/N above 50. A long-term
  floor is not inferred.
- **ELODIE:** the 1995 51 Pegasi result, 1996 instrument paper, later survey
  work and 2006 replacement by SOPHIE are treated as different evidence.
- **PARAS-1:** the full recorded range, the narrower RV-analysis range,
  selected bright-standard repeatability and uranium calibration remain
  separate. PARAS-1 and PARAS-2 are separate hardware records.

## General-purpose and legacy high-resolution instruments

- **HET HRS:** metre-per-second iodine results are conditional on target,
  mode and reduction. The later iodine-reference temperature discrepancy is a
  concrete reason to preserve calibration versions.
- **Hamilton:** the 25-year release contains more than 14,000 velocities for
  386 stars, but crosses hardware improvements and the final iodine-cell
  failure. The survey ending does not by itself prove hardware retirement.
- **Tull:** TS11, TS12, TS21 and TS23 are configurations of one facility
  instrument. Very-high-resolution TS12 spectra validated iodine structure;
  resolving power is not relabelled as RV accuracy.
- **HIDES:** the 6–8 m/s most-stable giant-survey result coexists with typical stellar
  scatter of 10–20 m/s. Slit and fibre-feed epochs require different
  illumination and line-spread-function treatment.
- **SALT HRS:** the 2026 call documents continuing operation and a current
  extraction limitation: measured HR resolving power is below the nominal
  mode because tilted lines are not fully modelled. Default automatic-pipeline
  accuracy and dedicated iodine performance are different quantities.

## Historical velocity systems

- **CES:** resolving power up to roughly 235,000 was achieved in narrow
  settings, but this is not a long-term velocity-accuracy claim.
- **CORAVEL:** a scanned physical mask produced a correlation dip. Published
  0.5–0.9 km/s examples belong to specific targets and programmes and should
  not be compared directly with CCD echelle EPRV statistics.

## Four physical NRES units

CTIO, McDonald, SAAO and Wise are separate records and map points even though
they share instrument design and pipeline software. LCO states that NRES is no
longer offered from semester 2026B. The Wise status page additionally gives a
unit-specific decommissioning date of 1 August 2026; that label is not copied
to the other three units. Network-level values of approximately 10–20 m/s in
the selected sources remain distinct from the 3 m/s design goal.

## Reproducible visual comparisons

The state-of-art figure separates on-sky examples from requirements,
commissioning and calibration values. The ideal detectability figure evaluates

\[
K=\left(\frac{2\pi G}{P}\right)^{1/3}
\frac{M_p\sin i}{(M_\star+M_p)^{2/3}}\frac{1}{\sqrt{1-e^2}}
\]

for the explicit circular, edge-on scenarios in
`data/detectability_scenarios.csv`. The curves exclude stellar variability,
cadence, weather, instrumental systematics and model-selection errors. They
explain signal scale; they do not predict a detection rate.

The complete paper-to-dossier links are machine-readable in
`data/instrument_dossiers.json` and the fifty `data/*_papers.csv` tables.
