"""Repository-native figures generated exclusively from committed CSV data."""
from __future__ import annotations

import math
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


def plot_expres_paired_metrics(metrics: pd.DataFrame, output: str | Path) -> None:
    """Plot only before/after values reported within the same paper and context."""
    fig, axes = plt.subplots(1, len(metrics), figsize=(10, 5), squeeze=False)
    for axis, row in zip(axes[0], metrics.itertuples(), strict=True):
        values = [row.before_mps, row.after_mps]
        axis.plot([0, 1], values, color="#174ea6", linewidth=2.5, marker="o", markersize=8)
        for index, value in enumerate(values):
            offset = (7, 9) if index == 0 else (-7, 9)
            alignment = "left" if index == 0 else "right"
            axis.annotate(f"{value:.2f} m/s", (index, value), xytext=offset,
                          textcoords="offset points", ha=alignment, fontweight="bold")
        axis.set_xticks([0, 1], ["Published baseline", "Published method"])
        axis.set_title(row.label, fontsize=10, wrap=True)
        axis.set_ylim(0, max(values) * 1.25)
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("EXPRES before/after results within their original measurement contexts")
    fig.supxlabel("These panels are not comparable instrument rankings")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_state_of_art_evidence(claims: pd.DataFrame, output: str | Path) -> None:
    """Separate achieved/on-sky examples from requirements and calibration floors."""
    achieved = claims[claims["measurement_context"].str.startswith("on-sky")].copy()
    reference = claims[~claims.index.isin(achieved.index)].copy()
    fig, axes = plt.subplots(1, 2, figsize=(15, 9), sharex=True)
    panels = [
        (axes[0], achieved.sort_values("value_mps"), "Published on-sky examples"),
        (axes[1], reference.sort_values("value_mps"), "Requirements, commissioning and calibration"),
    ]
    for axis, frame, title in panels:
        colours = ["#0f766e" if value < 1 else "#2563eb" for value in frame.value_mps]
        axis.barh(range(len(frame)), frame.value_mps, color=colours, edgecolor="#0f172a")
        axis.set_yticks(range(len(frame)), frame.instrument + " · " + frame.metric.str.replace("_", " "))
        axis.set_xscale("log")
        axis.axvline(1.0, color="#c2410c", linestyle="--", linewidth=1.4)
        axis.axvline(0.3, color="#7c3aed", linestyle=":", linewidth=1.6)
        axis.set_title(title)
        axis.grid(axis="x", which="both", alpha=0.2)
    axes[0].set_xlabel("Reported scale (m/s; metrics remain non-equivalent)")
    axes[1].set_xlabel("Reported scale (m/s; not achieved unless source says so)")
    fig.suptitle("Precision-RV evidence snapshot: measurement context before comparison")
    fig.text(0.5, 0.015, "Dashed: 1 m/s reference · dotted: 0.3 m/s reference", ha="center")
    fig.tight_layout(rect=(0, 0.035, 1, 0.96))
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_keplerian_detectability(scenarios: pd.DataFrame, output: str | Path) -> None:
    """Plot ideal circular-orbit semi-amplitudes from explicit committed assumptions."""
    gravitational_constant = 6.67430e-11
    earth_mass_kg = 5.9722e24
    solar_mass_kg = 1.98847e30
    day_seconds = 86400.0
    periods = [10 ** (-0.3 + index * (3.3 / 179)) for index in range(180)]
    fig, ax = plt.subplots(figsize=(11, 7))
    palette = ["#082f49", "#0284c7", "#9a3412", "#f97316"]
    for colour, row in zip(palette, scenarios.itertuples(), strict=True):
        planet_mass = row.planet_mass_earth * earth_mass_kg
        stellar_mass = row.stellar_mass_solar * solar_mass_kg
        values = []
        for period_days in periods:
            period = period_days * day_seconds
            amplitude = ((2 * math.pi * gravitational_constant / period) ** (1 / 3)
                         * planet_mass * row.sin_inclination
                         / ((stellar_mass + planet_mass) ** (2 / 3))
                         / math.sqrt(1 - row.eccentricity ** 2))
            values.append(amplitude)
        ax.plot(periods, values, color=colour, linewidth=2.4,
                linestyle="--" if row.line_style == "dashed" else "-", label=row.scenario)
    for value, label in [(1.0, "1 m/s"), (0.3, "30 cm/s"), (0.1, "10 cm/s")]:
        ax.axhline(value, color="#475569", linewidth=1, linestyle=":" )
        ax.text(1100, value * 1.05, label, ha="right", va="bottom", fontsize=9,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8})
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(periods), max(periods))
    ax.set_xlabel("Orbital period, P (days)")
    ax.set_ylabel("Ideal Keplerian semi-amplitude, K (m/s)")
    ax.set_title("Why sub-m/s radial velocities matter")
    ax.grid(which="both", alpha=0.2)
    ax.legend(frameon=False, loc="lower left")
    fig.text(0.5, 0.01, "Circular, edge-on examples; stellar variability, cadence and instrument systematics are not included.", ha="center")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(output, dpi=180)
    plt.close(fig)
