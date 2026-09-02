# Research source record

This file records the reasoning boundary behind `docs/REPORT.md`. The public
report is the readable synthesis; `data/performance_claims.csv` is the
claim-level evidence record.

## Question decomposition

1. Which physical instruments belong in a defensible precision-RV core?
2. What does each published numerical result measure?
3. What is each instrument's current operational state?
4. Which coupled errors prevent routine 0.10 m/s stellar accuracy over years?
5. Which candidates remain outside the comparison and why?

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
