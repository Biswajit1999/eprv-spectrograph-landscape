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
    assert len(df) == 21
    assert df["instrument"].is_unique
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
    assert len(claims) == 22
    assert claims["instrument"].nunique() == 21


def test_broader_census_is_structurally_valid():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    assert len(records) == 53
    assert len({row["instrument_id"] for row in records}) == 53
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
    assert by_id["keck-hires"]["current_status"] == "operational_planned_decommissioning"
    assert by_id["aat-veloce"]["current_status"] == "shared_risk"
    assert by_id["gemini-south-ghost"]["current_status"] == "operational_prv_mode_not_offered"


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
    assert len(paper_ids) == len(papers) == 241
    assert papers["source_url"].str.startswith("https://").all()
    assert papers["numerical_result"].str.len().min() >= 20
    assert "PARAS-2010-FIRSTLIGHT" in paper_ids
    assert "HIDES-2005-SURVEY" in paper_ids
    assert "PARAS-2011-FIRSTRESULTS" not in paper_ids
    assert "HIDES-2007-SURVEY" not in paper_ids
    assert "10.1088/0004-637X/744/1/54" not in " ".join(papers["source_url"])
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
    assert len(dossiers) == 53
    assert {item["instrument_id"] for item in dossiers} == census_ids
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
        "keck-hires",
        "paranal-uves",
        "ctio-chiron",
        "not-fies",
        "gemini-south-ghost",
        "aat-veloce",
        "aat-hermes",
        "aat-ucles",
        "cfht-espadons",
        "flwo-tres",
        "gemini-south-igrins",
        "lasilla-coralie",
        "lasilla-feros",
        "lasilla-fideos",
        "lbt-pepsi",
        "subaru-hds",
        "boao-boes",
        "calaralto-cafe",
        "eso-ces",
        "eso-coravel",
        "het-hrs",
        "lick-hamilton",
        "mcdonald-tull",
        "ohp-elodie",
        "okayama-hides",
        "lco-nres-ctio",
        "lco-nres-mcdonald",
        "lco-nres-saao",
        "lco-nres-wise",
        "prl-paras",
        "salt-hrs",
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
    assert all(item["mathml"].startswith("<math") for item in guide["equations"])
    assert all(item["source_url"].startswith("https://") for item in guide["steps"])
    by_name = {item["name"]: item for item in guide["comparators"]}
    assert "Gaia RVS" in by_name
    assert "JWST NIRSpec" in by_name
    assert all(not item["belongs_in_census"] for item in guide["taxonomy"] if "space" in item["class_name"].lower() or "survey" in item["class_name"].lower())


def test_salt_hrs_has_dated_current_status_evidence():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    salt = next(row for row in records if row["instrument_id"] == "salt-hrs")
    assert salt["current_status"] == "operational"
    assert salt["status_as_of"] == "2026-2"
    assert not salt["unresolved_fields"]


def test_paras_primary_source_is_the_actual_first_light_paper():
    records = load_census("data/census_registry.jsonl", "data/facilities.jsonl")
    paras = next(row for row in records if row["instrument_id"] == "prl-paras")
    assert paras["primary_source_url"] == "https://arxiv.org/abs/1007.4280"


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


def test_website_uses_natural_earth_geometry_not_schematic_shapes():
    html = Path("website/index.html").read_text(encoding="utf-8")
    script = Path("website/src/main.js").read_text(encoding="utf-8")
    package = json.loads(Path("website/package.json").read_text(encoding="utf-8"))
    assert "Natural Earth 1:110 million" in html
    assert 'id="map-countries"' in html
    assert "@cublya/world-atlas/countries-110m.json" in script
    assert "geoNaturalEarth1" in script
    assert "M44 112 92 78" not in html
    assert "@cublya/world-atlas" in package["dependencies"]


def test_site_frames_the_work_as_an_independent_literature_synthesis():
    html = Path("website/index.html").read_text(encoding="utf-8")
    script = Path("website/src/main.js").read_text(encoding="utf-8")

    assert "literature review while working on the EXOhSPEC testbed" in html
    assert "has not been formally validated by every principal investigator" in html
    assert "Independent literature synthesis" in html
    assert "Visit Academic Portfolio" in html
    assert "https://github.com/Biswajit1999" in html
    assert "https://www.linkedin.com/in/biswajit-jana-27011a151/" in html
    assert "https://orcid.org/0009-0002-2411-1891" in html
    assert "Content checked through" not in html
    assert "Updated 10 October 2026" not in html
    assert "Independent research software" not in html
    assert "EXOhSPEC is the practical origin of this literature study" in script
    assert "earlier designs, prototypes and subsystem experiments" in script
    assert "do not validate the present instrument configuration" in script


def test_site_explains_extraction_validation_and_claim_counts():
    html = Path("website/index.html").read_text(encoding="utf-8")
    assert "The pipeline is part of the measurement" in html
    assert "Cross-correlation function" in html
    assert "Template matching and forward models" in html
    assert "Why solar feeds matter" in html
    assert "21 instruments and 22 source-linked numerical records" in html
    assert "effectively infinite signal-to-noise and perfect detector sampling" in html


def test_site_leads_with_a_context_separated_eprv_landscape_atlas():
    html = Path("website/index.html").read_text(encoding="utf-8")
    assert "Where precision-RV spectrographs sit" in html
    assert "eprv_landscape_atlas.png" in html
    assert "on-sky measurements separate from requirements" in html
    assert "These values are not interchangeable performance scores" in html


def test_every_site_image_has_descriptive_alt_text():
    import re

    html = Path("website/index.html").read_text(encoding="utf-8")
    image_tags = re.findall(r"<img\b[^>]*>", html)
    assert image_tags
    for tag in image_tags:
        match = re.search(r'alt="([^"]+)"', tag)
        assert match, tag
        assert len(match.group(1).strip()) >= 30, tag


def test_site_exposes_paper_notes_map_detail_and_full_resolution_figures():
    html = Path("website/index.html").read_text(encoding="utf-8")
    script = Path("website/src/main.js").read_text(encoding="utf-8")
    assert "Precision RV Spectrograph Literature Atlas" in html
    assert 'id="map-detail"' in html
    assert 'id="figure-dialog"' in html
    assert html.count('class="figure-open"') == 8
    assert 'id="paper-count"' in html
    assert 'class="mobile-navigation"' in html
    assert "Paper-by-Paper" in script
    assert "Author's Proposed Follow-up" in script
    assert "Source trail summary" in script
    assert "reviewed ${esc(paper.reviewed_on)}" in script
    assert "Questions, Results and Remaining Tests" in script
