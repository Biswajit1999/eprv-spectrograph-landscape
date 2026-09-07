import json

import pandas as pd
import pytest

from eprv_landscape.data import (
    load_census,
    load_expres_metrics,
    load_expres_papers,
    load_instruments,
    load_performance_claims,
)


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


def test_expres_reading_list_and_paired_metrics_are_linked():
    papers = load_expres_papers("data/expres_papers.csv")
    metrics = load_expres_metrics("data/expres_metrics.csv", papers)
    assert len(papers) >= 12
    assert {2016, 2020, 2026} <= set(papers["year"])
    assert set(metrics["paper_id"]).issubset(set(papers["paper_id"]))
    assert (metrics["after_mps"] < metrics["before_mps"]).all()


def test_expres_dossier_is_explicitly_a_proposal_not_a_claim():
    with open("data/instrument_dossiers.json", encoding="utf-8") as source:
        dossiers = json.load(source)
    expres = next(item for item in dossiers if item["instrument_id"] == "lowell-expres")
    assert expres["paper_count"] == len(expres["paper_ids"])
    assert "proposal for discussion" in expres["candidate_project"]["status"]
    assert "not a complete bibliography" in expres["reading_boundary"]


def test_beginner_guide_has_sources_boundaries_and_taxonomy():
    with open("data/beginner_guide.json", encoding="utf-8") as source:
        guide = json.load(source)
    assert len(guide["steps"]) == 5
    assert len(guide["techniques"]) >= 3
    assert len(guide["equations"]) >= 3
    assert all(item["source_url"].startswith("https://") for item in guide["steps"])
    by_name = {item["name"]: item for item in guide["comparators"]}
    assert "Gaia RVS" in by_name
    assert "JWST NIRSpec" in by_name
    assert all(not item["belongs_in_census"] for item in guide["taxonomy"] if "space" in item["class_name"].lower() or "survey" in item["class_name"].lower())
