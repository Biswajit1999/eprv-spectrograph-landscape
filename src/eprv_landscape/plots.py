"""Repository-native figures generated exclusively from committed CSV data."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

STATUS_COLOURS = {
    "operational": "#2a9d8f",
    "operational_with_caveat": "#e9c46a",
    "offline": "#e76f51",
    "commissioning": "#457b9d",
    "planned": "#8d99ae",
    "legacy": "#64748b",
}


def plot_wavelength_coverage(df: pd.DataFrame, output: str | Path) -> None:
    ordered = df.sort_values(["wave_min_nm", "wave_max_nm"]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    for index, row in ordered.iterrows():
        ax.barh(index, row.wave_max_nm - row.wave_min_nm, left=row.wave_min_nm,
                color=STATUS_COLOURS[row.status], edgecolor="#17212b")
    ax.set_yticks(range(len(ordered)), ordered["instrument"])
    ax.set_xlabel("Nominal simultaneous wavelength coverage (nm)")
    ax.set_title("Spectral coverage and operational status")
    ax.grid(axis="x", alpha=0.25)
    ax.invert_yaxis()
    statuses = list(dict.fromkeys(ordered["status"]))
    ax.legend(handles=[Patch(facecolor=STATUS_COLOURS[s], label=s.replace("_", " ")) for s in statuses],
              loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_resolution_coverage(df: pd.DataFrame, output: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    offsets = {
        "HARPS-N": (8, -2), "HARPS3": (8, 8), "EXPRES": (8, 8),
        "ESPRESSO": (8, -16), "ANDES": (8, 6),
    }
    for row in df.itertuples():
        ax.scatter(row.wave_max_nm - row.wave_min_nm, row.resolving_power,
                   color=STATUS_COLOURS[row.status], s=65)
        ax.annotate(row.instrument, (row.wave_max_nm - row.wave_min_nm, row.resolving_power),
                    xytext=offsets.get(row.instrument, (6, 6)), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Nominal wavelength span (nm)")
    ax.set_ylabel("Representative resolving power, R")
    ax.set_title("Resolution versus spectral grasp (not a performance ranking)")
    ax.grid(alpha=0.25)
    statuses = list(dict.fromkeys(df["status"]))
    ax.legend(handles=[Patch(facecolor=STATUS_COLOURS[s], label=s.replace("_", " ")) for s in statuses],
              loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_claim_context(claims: pd.DataFrame, output: str | Path) -> None:
    """Plot reported velocity scales while making non-equivalent contexts visible."""
    context_colours = {
        "design requirement": "#94a3b8",
        "engineering requirement": "#94a3b8",
        "subsystem calibration validation": "#f59e0b",
        "on-sky commissioning": "#7c3aed",
        "commissioning stellar exposure": "#7c3aed",
        "on-sky high-SNR spectra": "#0f766e",
        "on-sky solar feed": "#0284c7",
        "on-sky solar time series": "#0284c7",
    }
    ordered = claims.sort_values("value_mps", ascending=False).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 9))
    colours = [context_colours.get(value, "#2563eb") for value in ordered.measurement_context]
    ax.barh(ordered.index, ordered.value_mps, color=colours, edgecolor="#0f172a")
    ax.set_yticks(ordered.index, ordered.instrument + " · " + ordered.metric.str.replace("_", " "))
    ax.set_xscale("log")
    ax.set_xlabel("Reported velocity scale (m/s, logarithmic axis)")
    ax.set_title("Published numbers describe different experiments — not an instrument ranking")
    ax.grid(axis="x", which="both", alpha=0.22)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)
