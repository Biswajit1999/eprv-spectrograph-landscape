from eprv_landscape.analysis import claim_context_summary, spectral_coverage_summary, status_summary
from eprv_landscape.data import load_instruments, load_performance_claims


def test_coverage_span_is_positive():
    result = spectral_coverage_summary(load_instruments("data/instruments.csv"))
    assert (result["wavelength_span_nm"] > 0).all()


def test_status_counts_preserve_denominator():
    df = load_instruments("data/instruments.csv")
    assert status_summary(df)["n_instruments"].sum() == len(df)


def test_claim_context_counts_preserve_denominator():
    instruments = load_instruments("data/instruments.csv")
    claims = load_performance_claims("data/performance_claims.csv", instruments)
    assert claim_context_summary(claims)["n_claims"].sum() == len(claims)
