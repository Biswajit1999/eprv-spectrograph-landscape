# Reproducibility

From a clean checkout with Python 3.10 or newer:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# POSIX shell: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
eprv-landscape build --data data/instruments.csv --claims data/performance_claims.csv --out results
```

The build validates controlled vocabularies, claim identifiers, numeric values,
claim-to-instrument references, the EXPRES paper list and its paired figure
values, then regenerates every file under `results/`.
The test suite also validates `data/census_registry.jsonl` against
`data/facilities.jsonl`, resolves every dossier paper identifier, checks that all
53 census instruments have dossiers, and guards corrected PARAS and HIDES source
records. The figure set includes the idealized scenarios committed in
`data/detectability_scenarios.csv`; those curves are not fitted to observations.

The build also regenerates the 15-scenario Doppler-information study from
`data/information_experiment_scenarios.csv`. Four scenarios run 1,000 seeded
Poisson trials. Tests check analytic photon scaling, the expected broadening
order, the predeclared diminishing-return condition, recovery calibration,
output schema and byte-for-byte agreement between generated results and the
website copies. After rebuilding, copy the two generated assets before a site
release:

```powershell
Copy-Item results/figures/doppler_information_experiment.png website/public/figures/
Copy-Item results/doppler_information_experiment.csv website/public/data/
```

Build and serve the static website:

```bash
cd website
npm ci
npm run build
npm run preview
```

The Vite build uses relative asset and data paths so the same artifact works at
the GitHub Pages repository subpath. `.github/workflows/pages.yml` publishes
`website/dist` after a successful push to `main`.
