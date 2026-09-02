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

Serve the static website with `python -m http.server 8000` and open
`http://localhost:8000/site/`. It also works when `site/index.html` is opened
directly in a modern browser.
