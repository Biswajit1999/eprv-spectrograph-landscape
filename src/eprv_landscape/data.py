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
    if df[["primary_reference", "status_source", "status_as_of"]].isna().any().any():
        raise ValueError("every row requires dated scientific and status provenance")
    return df
