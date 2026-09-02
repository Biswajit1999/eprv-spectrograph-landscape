"""Validated loading of the curated instrument and evidence tables."""
from __future__ import annotations

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
        raise ValueError("every row requires dated scientific and status provenance")
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
