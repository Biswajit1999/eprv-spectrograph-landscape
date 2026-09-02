"""Descriptive comparisons that avoid false precision rankings."""
from __future__ import annotations

import pandas as pd


def status_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Count instruments by explicitly dated operational-status category."""
    return df.groupby("status", dropna=False).size().rename("n_instruments").reset_index()


def spectral_coverage_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return wavelength span and coverage ratio without treating them as merit scores."""
    result = df[["instrument", "wave_min_nm", "wave_max_nm", "resolving_power"]].copy()
    result["wavelength_span_nm"] = result["wave_max_nm"] - result["wave_min_nm"]
    result["wavelength_ratio"] = result["wave_max_nm"] / result["wave_min_nm"]
    return result.sort_values("wave_min_nm").reset_index(drop=True)


def performance_evidence_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Count evidence classes; intentionally does not rank free-text performance claims."""
    return (
        df.groupby("performance_class", dropna=False).size()
        .rename("n_instruments").reset_index().sort_values("performance_class")
    )
