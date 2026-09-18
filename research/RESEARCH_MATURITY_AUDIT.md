# Research maturity audit: before and after v0.15.0

Audit date: 2026-09-18

The comparison uses ten dimensions scored from 0 to 10. Scores represent
evidence present in the repository, not prestige, publication status or the
scientific value of an instrument team. The machine-readable rubric is in
`research/RESEARCH_MATURITY_AUDIT.csv`.

| Dimension | Before | After | Material change |
|---|---:|---:|---|
| Falsifiable question and hypotheses | 6 | 10 | Executed null, alternative and threshold |
| Primary literature and provenance | 10 | 10 | Method source added; existing 241-source graph retained |
| Data and schema discipline | 9 | 9 | Versioned scenarios and results added |
| Independent scientific analysis | 3 | 8 | 15-scenario Fisher-information experiment |
| Uncertainty and statistical calibration | 3 | 8 | Analytic bound plus Monte Carlo uncertainty and coverage |
| Ground-truth recovery tests | 0 | 9 | Four 1,000-trial seeded injection-recovery validations |
| Automated and numerical testing | 7 | 9 | 20 to 27 passing tests |
| Reproducible environments and CI | 7 | 9 | One Python version to a 3.10/3.12/3.13 matrix |
| Claim and limitation discipline | 9 | 10 | Generated claims and explicit synthetic-to-real boundary |
| Research dissemination | 9 | 10 | Study, data and figure published through the site |
| **Total** | **63/100** | **92/100** | **Literature guide plus independently validated experiment** |

The score does not claim a literal tenfold increase: the repository already had
excellent literature provenance and documentation. The substantive upgrade is
concentrated where the baseline was weakest—executed hypotheses, independent
analysis, uncertainty calibration and ground-truth recovery.
