# Instrument-evidence completeness sensitivity (conditional)

This isolated Python module computes three complementary diagnostics: facility-level counts of instrument records with primary references and dated status sources; descriptive Wilson intervals for binary coverage fractions; and leave-one-facility-out complete-evidence fractions. It does **not** rank instrument performance or alter the catalogue.

Inputs must be explicit, unique (facility, instrument) pairs with two verified boolean fields. The module does not scrape, infer, or validate source links, and does not operate on the published catalogue until a documented field mapping is approved. The Wilson interval assumes independent Bernoulli records and is not appropriate as a calibrated population confidence interval for clustered facilities or a non-random catalogue. Facility deletion is descriptive sensitivity, not uncertainty quantification. No observational conclusions follow from the synthetic fixtures.

Reproduce: `PYTHONPATH=. python -m pytest -q tests/test_evidence_sensitivity.py`. Before any catalogue application, verify primary-source mapping, missing-value policy and duplicate identities against `docs/METHODS.md`; run the repository-required `pytest -q`, `ruff check src tests`, and `eprv-landscape build`.

Development disclosure: AI-assisted code and tests prepared for scientific review; Biswajit Jana is the requested authenticated Git author, with no co-authors asserted.
