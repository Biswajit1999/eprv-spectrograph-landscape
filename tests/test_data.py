import json

import pandas as pd
import pytest

from eprv_landscape.data import load_census, load_instruments, load_performance_claims


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


def test_performance_claims_are_linked_and_caveated():
    instruments = load_instruments("data/instruments.csv")
    claims = load_performance_claims("data/performance_claims.csv", instruments)
    assert claims["claim_id"].is_unique
    assert set(claims["instrument"]).issubset(set(instruments["instrument"]))
    assert claims["caveat"].str.len().min() >= 10
    assert claims["source_url"].str.startswith(("https://", "http://")).all()


def test_broader_census_is_structurally_valid():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    assert len(records) >= 50
    assert all(row["entity_type"] == "physical_instrument" for row in records)


def test_nres_units_are_physical_records_and_exohspec_is_present():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    by_id = {row["instrument_id"]: row for row in records}
    nres = [row for row in records if row["acronym"] == "NRES"]
    assert len(nres) == 4
    assert len({row["facility_id"] for row in nres}) == 4
    assert by_id["lco-nres-wise"]["current_status"] == "decommissioned"
    assert by_id["tno-exohspec"]["current_status"] == "installed_testing"


def test_status_corrections_are_not_overstated():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    by_id = {row["instrument_id"]: row for row in records}
    assert by_id["ing-harps3"]["current_status"] == "commissioning_shared_risk"
    assert by_id["palomar-parvi"]["current_status"] == "status_conflict"


def test_challenge_profiles_are_cited_and_complete():
    with open("data/challenge_profiles.json", encoding="utf-8") as source:
        profiles = json.load(source)
    assert len(profiles) == 9
    assert len({profile["id"] for profile in profiles}) == 9
    for profile in profiles:
        assert all(profile[field] for field in ("mechanism", "evidence", "mitigation", "residual"))
        assert len(profile["sources"]) >= 2
        assert all(source["url"].startswith("https://") for source in profile["sources"])
