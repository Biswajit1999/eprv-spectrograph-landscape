# Claim ledger

All quantitative performance statements map to
`data/performance_claims.csv`. `PERF-001` through `PERF-022` identify the source,
metric, value, sample, baseline and caveat. Derived counts map to
`results/manifest.json` and the summary CSV files.

| Statement | Evidence |
|---|---|
| 21 instruments, 22 quantitative claims, 13 EXPRES papers, six HARPS sources and seven ESPRESSO sources | `results/manifest.json` |
| 53 physical census records across 33 represented facilities | `data/census_registry.jsonl`, validated against `data/facilities.jsonl` |
| HARPS near 1 m/s | `PERF-001` |
| HARPS-N 1.27 to 1.07 m/s | `PERF-002` plus cited paper |
| SOPHIE+ 1–2 m/s | `PERF-003` |
| APF 1.35 m/s | `PERF-004` |
| ESPRESSO about 0.10 m/s photon limit | `PERF-005` |
| EXPRES below 0.10 m/s calibration; 0.895 m/s residual | `PERF-006`, `PERF-007` |
| CARMENES 1.6 m/s | `PERF-008` |
| iSHELL few-m/s result | `PERF-009` |
| IRD below 2 m/s | `PERF-010` |
| HPF about 1.5 m/s | `PERF-011` |
| PFS below 1 m/s | `PERF-012` |
| SPIRou about 2 m/s | `PERF-013` |
| PARVI 4–10 m/s | `PERF-014` |
| MAROON-X about 0.30 m/s short-term floor | `PERF-015` |
| NEID 0.41–0.66 m/s solar RMS | `PERF-016` |
| KPF 0.50 m/s requirement, 0.30 m/s goal | `PERF-017` plus source |
| PARAS-2 2.65 m/s | `PERF-018` |
| NIRPS below 1 m/s commissioning result | `PERF-019` |
| HARPS3, ANDES, G-CLEF 0.10 m/s goals | `PERF-020`–`PERF-022` |
| EXPRES paired values: 1.17 to 1.05 m/s and 1.32 to 0.43 m/s | `data/expres_metrics.csv`, linked to `EXP-2021-EXCALIBUR` and `EXP-2026-SYSTEMATICS` |

The wider EXPRES reading statements are mapped paper by paper in
`data/expres_papers.csv`; interpretation and proposal boundaries are stated in
`docs/EXPRES_READING_NOTE.md`.

The HARPS commissioning, calibration and hardware-era statements are mapped in
`data/harps_papers.csv`; their contexts and the boundary around the proposed
era-transfer study are stated in `docs/HARPS_READING_NOTE.md`.

ESPRESSO statements are mapped in `data/espresso_papers.csv`; the distinction
between differential precision, wavelength accuracy and end-to-end validation
is maintained in `docs/ESPRESSO_READING_NOTE.md`.

The values are not averaged, scored or ranked because their definitions differ.
