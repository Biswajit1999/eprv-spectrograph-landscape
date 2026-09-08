import json
from pathlib import Path

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
    assert by_id["tno-exohspec"]["current_status"] == "status_conflict"


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


def test_instrument_dossiers_resolve_papers_and_label_future_analysis():
    with open("data/instrument_dossiers.json", encoding="utf-8") as source:
        dossiers = json.load(source)
    paper_files = sorted(Path("data").glob("*_papers.csv"))
    papers = pd.concat([pd.read_csv(path) for path in paper_files], ignore_index=True)
    paper_ids = set(papers["paper_id"])
    assert len(paper_ids) == len(papers) == 125
    assert papers["source_url"].str.startswith("https://").all()
    assert papers["numerical_result"].str.len().min() >= 20
    for dossier in dossiers:
        assert dossier["paper_count"] == len(dossier["paper_ids"])
        assert set(dossier["paper_ids"]) <= paper_ids
        assert "not completed research" in dossier["future_analysis"]["status"]
        assert "first_conversation" not in dossier["future_analysis"]

    expres = next(item for item in dossiers if item["instrument_id"] == "lowell-expres")
    assert "not a complete bibliography" in expres["reading_boundary"]
    harps = next(item for item in dossiers if item["instrument_id"] == "lasilla-harps")
    assert harps["paper_count"] == 6
    assert "final report" in harps["latest_problem"]
    espresso = next(item for item in dossiers if item["instrument_id"] == "paranal-espresso")
    assert espresso["paper_count"] == 7
    assert "precision with absolute accuracy" in espresso["future_analysis"]["question"]
    harpsn = next(item for item in dossiers if item["instrument_id"] == "tng-harpsn")
    assert harpsn["paper_count"] == 6
    assert "signal-preservation" in harpsn["future_analysis"]["title"]
    neid = next(item for item in dossiers if item["instrument_id"] == "wiyn-neid")
    assert neid["paper_count"] == 7
    assert "master-file versions" in neid["future_analysis"]["success_tests"][-1]
    exohspec = next(item for item in dossiers if item["instrument_id"] == "tno-exohspec")
    assert exohspec["paper_count"] == 7
    assert "No completed on-sky stellar-RV" in exohspec["reading_boundary"]
    assert "conflict" in exohspec["current_status"].lower()
    census_ids = {
        row["instrument_id"] for row in load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    }
    assert len(dossiers) == 22
    assert {item["instrument_id"] for item in dossiers} <= census_ids
    for instrument_id in (
        "keck-kpf",
        "gemini-north-maroonx",
        "calaralto-carmenes",
        "het-hpf",
        "cfht-spirou",
        "lasilla-nirps",
        "magellan-pfs",
        "ohp-sophie",
        "lick-apf-levy",
        "irtf-ishell",
        "subaru-ird",
        "palomar-parvi",
        "prl-paras2",
        "ing-harps3",
        "elt-andes",
        "gmt-gclef",
    ):
        assert next(item for item in dossiers if item["instrument_id"] == instrument_id)


def test_harpsn_now_has_a_dated_current_status_source():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    harpsn = next(row for row in records if row["instrument_id"] == "tng-harpsn")
    assert harpsn["current_status"] == "operational"
    assert harpsn["status_source_url"] == "https://tngweb.tng.iac.es/call/info.html"
    assert not harpsn["unresolved_fields"]


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


def test_every_represented_facility_has_a_source_linked_map_coordinate():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    with open("data/facilities.jsonl", encoding="utf-8") as source:
        facilities = [json.loads(line) for line in source if line.strip()]
    represented = {row["facility_id"] for row in records}
    mapped = {row["facility_id"]: row for row in facilities if row["facility_id"] in represented}
    assert set(mapped) == represented
    for facility in mapped.values():
        assert -90 <= facility["latitude_deg"] <= 90
        assert -180 <= facility["longitude_deg"] <= 180
        assert facility["coordinate_source_url"].startswith("https://")
