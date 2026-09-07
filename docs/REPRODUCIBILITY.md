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

The build validates controlled vocabularies, claim identifiers, numeric values
and claim-to-instrument references, then regenerates every file under `results/`.
The test suite also validates `data/census_registry.jsonl` against
`data/facilities.jsonl`.

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
