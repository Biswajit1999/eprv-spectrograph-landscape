import pandas as pd
import pytest

from eprv_landscape.data import load_instruments


def test_committed_instrument_table_is_valid():
    df = load_instruments("data/instruments.csv")
    assert len(df) >= 12
    assert {"optical", "near_infrared", "optical_and_near_infrared"} <= set(df.spectral_domain)


def test_rejects_reversed_wavelength_interval(tmp_path):
    source = pd.read_csv("data/instruments.csv").iloc[:1].copy()
    source.loc[:, "wave_min_nm"] = 900
    source.loc[:, "wave_max_nm"] = 400
    path = tmp_path / "bad.csv"
    source.to_csv(path, index=False)
    with pytest.raises(ValueError):
        load_instruments(path)


def test_rejects_uncontrolled_performance_category(tmp_path):
    source = pd.read_csv("data/instruments.csv").iloc[:1].copy()
    source.loc[:, "performance_class"] = "best"
    path = tmp_path / "bad.csv"
    source.to_csv(path, index=False)
    with pytest.raises(ValueError):
        load_instruments(path)
