from eprv_landscape.analysis import spectral_coverage_summary, status_summary
from eprv_landscape.data import load_instruments


def test_coverage_span_is_positive():
    result = spectral_coverage_summary(load_instruments("data/instruments.csv"))
    assert (result["wavelength_span_nm"] > 0).all()


def test_status_counts_preserve_denominator():
    df = load_instruments("data/instruments.csv")
    assert status_summary(df)["n_instruments"].sum() == len(df)
