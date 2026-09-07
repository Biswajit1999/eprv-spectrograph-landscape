"""Validated loading of the curated instrument and evidence tables."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

REQUIRED_INSTRUMENT_COLUMNS = {
    "instrument", "facility", "hemisphere", "wave_min_nm", "wave_max_nm",
    "resolving_power", "spectral_domain", "status", "status_as_of",
    "performance_class", "reported_performance", "primary_reference", "status_source",
}
ALLOWED_PERFORMANCE_CLASSES = {
    "design_requirement", "laboratory_calibration", "on_sky_stability",
    "commissioning_report", "not_comparably_reported",
}
ALLOWED_STATUSES = {
    "operational", "operational_with_caveat", "offline", "commissioning",
    "planned", "legacy",
}

CENSUS_REQUIRED_FIELDS = {
    "instrument_id", "official_name", "entity_type", "inclusion_tier",
    "facility_id", "telescope", "site", "physical_country_or_territory",
    "current_status", "primary_source_url", "official_instrument_url",
    "verification_state", "unresolved_fields", "notes",
}
CENSUS_TIERS = {
    "A_dedicated_prv_eprv",
    "B_general_high_resolution_with_rv_evidence",
    "C_historical_prototype_or_specialist",
    "D_funded_construction_or_commissioning",
}
CENSUS_VERIFICATION_STATES = {"verified", "partially_verified"}


def load_instruments(path: str | Path) -> pd.DataFrame:
    """Load and validate the source-traceable instrument table."""
    df = pd.read_csv(path)
    missing = REQUIRED_INSTRUMENT_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"missing instrument columns: {sorted(missing)}")
    if df["instrument"].duplicated().any():
        raise ValueError("instrument names must be unique")
    if (df["wave_min_nm"] >= df["wave_max_nm"]).any():
        raise ValueError("every wavelength interval must have positive width")
    if (df["resolving_power"] <= 0).any():
        raise ValueError("resolving_power must be positive")
    bad_classes = set(df["performance_class"]) - ALLOWED_PERFORMANCE_CLASSES
    if bad_classes:
        raise ValueError(f"unknown performance classes: {sorted(bad_classes)}")
    bad_statuses = set(df["status"]) - ALLOWED_STATUSES
    if bad_statuses:
        raise ValueError(f"unknown statuses: {sorted(bad_statuses)}")
    if df[["primary_reference", "status_source", "status_as_of"]].isna().any().any():
        raise ValueError("every row requires a dated scientific source and status source")
    return df


REQUIRED_CLAIM_COLUMNS = {
    "claim_id", "instrument", "metric", "value_mps", "comparison",
    "measurement_context", "target_or_sample", "baseline", "reported_result",
    "caveat", "source_url", "accessed",
}


def load_performance_claims(path: str | Path, instruments: pd.DataFrame) -> pd.DataFrame:
    """Load quantitative claims and enforce links to the instrument registry."""
    claims = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_CLAIM_COLUMNS - set(claims.columns)
    if missing:
        raise ValueError(f"missing performance-claim columns: {sorted(missing)}")
    if claims["claim_id"].duplicated().any():
        raise ValueError("claim identifiers must be unique")
    unknown = set(claims["instrument"]) - set(instruments["instrument"])
    if unknown:
        raise ValueError(f"claims reference unknown instruments: {sorted(unknown)}")
    values = pd.to_numeric(claims["value_mps"], errors="coerce")
    if values.isna().any() or (values <= 0).any():
        raise ValueError("performance values must be positive numbers")
    required_text = ["source_url", "reported_result", "caveat", "accessed"]
    if claims[required_text].eq("").any().any():
        raise ValueError("every claim requires a source, result, caveat and access date")
    return claims


REQUIRED_EXPRES_PAPER_COLUMNS = {
    "paper_id", "year", "title", "authors_short", "paper_type", "what_was_studied",
    "numerical_result", "remaining_question", "source_url", "reviewed_on",
}


def load_expres_papers(path: str | Path) -> pd.DataFrame:
    """Load the selected EXPRES reading list and reject incomplete paper notes."""
    papers = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_EXPRES_PAPER_COLUMNS - set(papers.columns)
    if missing:
        raise ValueError(f"missing EXPRES paper columns: {sorted(missing)}")
    if papers["paper_id"].duplicated().any():
        raise ValueError("EXPRES paper identifiers must be unique")
    if not papers["source_url"].str.startswith("https://").all():
        raise ValueError("every EXPRES paper requires an HTTPS primary-source URL")
    required = ["title", "what_was_studied", "numerical_result", "remaining_question"]
    if papers[required].eq("").any().any():
        raise ValueError("every EXPRES paper note requires a result and remaining question")
    return papers


def load_expres_metrics(path: str | Path, papers: pd.DataFrame) -> pd.DataFrame:
    """Load paired, within-paper EXPRES metrics used by the comparison figure."""
    metrics = pd.read_csv(path, keep_default_na=False)
    required = {
        "metric_id", "paper_id", "label", "before_mps", "after_mps", "context", "source_url"
    }
    missing = required - set(metrics.columns)
    if missing:
        raise ValueError(f"missing EXPRES metric columns: {sorted(missing)}")
    if metrics["metric_id"].duplicated().any():
        raise ValueError("EXPRES metric identifiers must be unique")
    unknown = set(metrics["paper_id"]) - set(papers["paper_id"])
    if unknown:
        raise ValueError(f"EXPRES metrics reference unknown papers: {sorted(unknown)}")
    for field in ("before_mps", "after_mps"):
        metrics[field] = pd.to_numeric(metrics[field], errors="raise")
        if (metrics[field] <= 0).any():
            raise ValueError(f"{field} values must be positive")
    return metrics


def load_jsonl(path: str | Path) -> list[dict]:
    """Load newline-delimited JSON and identify a malformed record by line number."""
    records = []
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number} of {path}") from exc
    return records


def load_census(path: str | Path, facilities_path: str | Path) -> list[dict]:
    """Validate the broader physical-instrument census and its facility references."""
    records = load_jsonl(path)
    facilities = load_jsonl(facilities_path)
    if not records:
        raise ValueError("census must contain at least one physical instrument")
    facility_ids = {row.get("facility_id") for row in facilities}
    if None in facility_ids or len(facility_ids) != len(facilities):
        raise ValueError("facility identifiers must be present and unique")
    instrument_ids = [row.get("instrument_id") for row in records]
    if None in instrument_ids or len(set(instrument_ids)) != len(instrument_ids):
        raise ValueError("instrument identifiers must be present and unique")
    for row in records:
        missing = CENSUS_REQUIRED_FIELDS - row.keys()
        if missing:
            raise ValueError(
                f"{row.get('instrument_id', '<unknown>')} is missing fields: {sorted(missing)}"
            )
        if row["entity_type"] != "physical_instrument":
            raise ValueError(f"{row['instrument_id']} is not a physical-instrument record")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row["instrument_id"]):
            raise ValueError(f"{row['instrument_id']} is not a stable slug identifier")
        if row["inclusion_tier"] not in CENSUS_TIERS:
            raise ValueError(f"{row['instrument_id']} has an unknown inclusion tier")
        if row["verification_state"] not in CENSUS_VERIFICATION_STATES:
            raise ValueError(f"{row['instrument_id']} has an unknown verification state")
        if row["facility_id"] not in facility_ids:
            raise ValueError(f"{row['instrument_id']} references an unknown facility")
        for field in ("primary_source_url", "official_instrument_url"):
            if not str(row[field]).startswith("https://"):
                raise ValueError(f"{row['instrument_id']} requires an HTTPS {field}")
        if row["verification_state"] == "partially_verified" and not row["unresolved_fields"]:
            raise ValueError(f"{row['instrument_id']} must state what remains unresolved")
    return records
