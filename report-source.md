# Research source record

This file records the reasoning boundary behind `docs/REPORT.md`. The public
report is the readable synthesis; `data/performance_claims.csv` is the
claim-level evidence record.

## Question decomposition

1. How does a beginner get from dispersed starlight to an RV time series?
2. Which physical instruments belong in a defensible precision-RV core?
3. What does each published numerical result measure?
4. What is each instrument's current operational state?
5. Which coupled errors prevent routine 0.10 m/s stellar accuracy over years?
6. Which candidates remain outside the comparison and why?

## Beginner-guide evidence boundary

The beginner chapter uses primary methods papers for photon information,
absorption-cell modelling, extraction, barycentric correction, stellar noise
and tellurics. Current official documentation is used for operational examples
and the Gaia RVS/JWST NIRSpec scope comparison. The small-shift Doppler equation
is explicitly labelled explanatory; it is not substituted for the relativistic
barycentric calculation. Resolving power is not described as RV accuracy, and
the Bouchy et al. photon limit is not described as long-baseline performance.

## Coverage decisions

- **Core:** the 19 current/upcoming systems in the 2026 Annual Review table.
- **Added:** ANDES and G-CLEF as planned systems; PARAS-2 as a documented
  operational regional system.
- **Not counted separately:** observing modes, detector upgrades, pipelines,
  survey programmes, telescope sites and individual papers.
- **Deferred:** a global historical census, facility coordinates, throughput
  curves, raw-spectrum re-reduction and a complete detector-era table.

## Evidence hierarchy

Peer-reviewed instrument/performance papers support historical quantitative
claims. Current observatory or consortium pages support status. A design value
cannot satisfy an achieved-performance claim. Search-result snippets were used
only to locate primary pages and are not evidence records.

## Consequential reconciliations

- KPF is recorded offline from Keck's dated status page, not operational from an
  older instrument paper.
- HARPS3 is commissioning/shared risk, not fully operational.
- PARVI is labelled legacy from the current Caltech laboratory page; its
  4–10 m/s commissioning result is retained rather than replaced by its goal.
- NRES is excluded from the detailed table pending unit-level records for its
  four physical spectrographs and current post-2026B offering state.
- Las Cumbres Observatory and Las Campanas Observatory are distinct facilities.

## Completion gate

The current release passes when all quantitative report statements appear in
`docs/CLAIMS.md`, all claim rows resolve to an instrument, every claim has a
caveat and source, generated results are reproducible, tests pass, and the site
build succeeds. It does not claim a saturated global census.

## EXPRES dossier question

How did the EXPRES literature move from design and commissioning to the current
long-baseline limitation, and what small software study could be discussed with
the team without overstating the published evidence?

The direct answer and paper-by-paper synthesis are maintained in
`docs/EXPRES_READING_NOTE.md`. The single source table is
`data/expres_papers.csv`; paired numerical values used in the original figure
are recorded separately in `data/expres_metrics.csv`.

The proposed era-aware correction audit is an inference from the validation gaps
identified in the 2022 method comparison and the diagnostics demonstrated in the
2026 long-baseline study. It is labelled as a candidate project, not attributed
to the source authors and not presented as completed work.
