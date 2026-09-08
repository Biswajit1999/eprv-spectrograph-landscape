# NEID reading note: illumination, solar baselines and RV eras

**Reviewed:** 8 September 2026  
**Scope:** Seven selected subsystem, operations, solar and pipeline sources. This
is not a complete bibliography of NEID exoplanet science.

## Direct answer

NEID covers 380–930 nm at R ≈ 112,000 in high-resolution mode and R ≈ 72,000
in high-efficiency mode. It was designed around a 0.27 m/s single-visit
instrumental requirement. The requirement should not be relabelled as achieved
stellar precision.

Subsystem results establish necessary conditions. A 30-day environmental test
maintained pressure below 10⁻⁶ Torr and temperature RMS below 0.4 mK. The fibre
paper explains why illumination changes can cause RV errors that a stable
wavelength reference cannot calibrate if stellar and reference light do not
share the relevant path. These results justify monitoring temperature,
illumination and exposure-meter data, but neither is an end-to-end stellar RMS.

The four-month solar-feed paper reports 0.66 m/s RMS under good conditions and
0.41 m/s for a best-condition subset. The 3.5-year release later identifies
117,060 observations unlikely to be significantly affected by weather, hardware
or major calibration problems. Those selections are useful, but a cleaned sample
count does not demonstrate preservation of a weak planet signal.

Current DRP 1.5.2 documentation provides a concrete software problem. It says
the high-S/N ThAr master has known systematics toward order edges because it
lacks LFC and Fabry–Pérot refinements. It also versions etalon lists around 2024
and 2025 changes and documents RV eras. Reduced velocities therefore need the
calibration-master and era identity carried with them.

## Selected evidence

- [Environmental-control test](https://arxiv.org/abs/1902.07729)
- [NEID solar-feed commissioning](https://arxiv.org/abs/2112.05711)
- [Exposure-control and operations software](https://arxiv.org/abs/2210.00550)
- [Fibre-illumination analysis](https://arxiv.org/abs/2307.12403)
- [Four-instrument solar comparison](https://arxiv.org/abs/2309.03762)
- [3.5-year solar release](https://arxiv.org/abs/2408.13318)
- [Current wavelength-master documentation](https://neid.ipac.caltech.edu/docs/NEID-DRP/masterfiles.html)

## Candidate project to discuss

A version-aware validation notebook would join each public solar and standard-
star product to its DRP version, RV era, wavelength master, etalon list and
observing conditions. It would examine residuals versus order position and
barycentric velocity, test the reported late-day cross-instrument trend, hold
out complete hardware eras, and verify injected wavelength-dependent shifts.

This is a proposal for discussion, dependent on archive products and confirmed
event metadata. It is not a completed correction or a statement of the NEID
team's priorities. Records are in `data/neid_papers.csv` and
`data/instrument_dossiers.json`.
