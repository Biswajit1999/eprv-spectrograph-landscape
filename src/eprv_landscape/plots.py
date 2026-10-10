"""Repository-native figures generated exclusively from committed CSV data."""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

from .plot_style import INK, MUTED, PALETTE, save_figure, scientific_plot

STATUS_COLOURS = {
    "operational": PALETTE["green"],
    "operational_with_caveat": PALETTE["orange"],
    "offline": PALETTE["vermilion"],
    "commissioning": PALETTE["blue"],
    "planned": PALETTE["purple"],
    "legacy": PALETTE["grey"],
}

BAND_COLOURS = {
    "optical": PALETTE["blue"],
    "near_infrared": PALETTE["vermilion"],
    "optical_and_near_infrared": PALETTE["green"],
}


def _claim_family(context: str) -> str:
    if context.startswith("on-sky solar"):
        return "Solar time series"
    if context.startswith("on-sky"):
        return "On-sky stellar"
    if "calibration" in context:
        return "Subsystem calibration"
    if "requirement" in context:
        return "Design / requirement"
    return "Commissioning"


@scientific_plot
def plot_wavelength_coverage(df: pd.DataFrame, output: str | Path) -> None:
    ordered = df.sort_values(["wave_min_nm", "wave_max_nm"]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    for index, row in ordered.iterrows():
        ax.barh(index, row.wave_max_nm - row.wave_min_nm, left=row.wave_min_nm,
                color=STATUS_COLOURS[row.status], edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(ordered)), ordered["instrument"])
    ax.set_xlabel("Nominal simultaneous wavelength coverage (nm)")
    ax.set_title("Spectral coverage and operational status")
    ax.grid(axis="x", which="major")
    ax.grid(axis="y", visible=False)
    ax.invert_yaxis()
    statuses = list(dict.fromkeys(ordered["status"]))
    ax.legend(handles=[Patch(facecolor=STATUS_COLOURS[s], label=s.replace("_", " ")) for s in statuses],
              loc="lower right", frameon=False)
    fig.tight_layout()
    save_figure(fig, output)


@scientific_plot
def plot_resolution_coverage(df: pd.DataFrame, output: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    offsets = {
        "HARPS-N": (8, -2), "HARPS3": (8, 8), "EXPRES": (8, 8),
        "ESPRESSO": (8, -16), "ANDES": (8, 6),
    }
    for row in df.itertuples():
        ax.scatter(row.wave_max_nm - row.wave_min_nm, row.resolving_power,
                   color=STATUS_COLOURS[row.status], edgecolor="white", linewidth=0.7, s=64)
        ax.annotate(row.instrument, (row.wave_max_nm - row.wave_min_nm, row.resolving_power),
                    xytext=offsets.get(row.instrument, (6, 6)), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Nominal wavelength span (nm)")
    ax.set_ylabel("Representative resolving power, R")
    ax.set_title("Resolution versus spectral grasp (not a performance ranking)")
    ax.grid(which="major")
    statuses = list(dict.fromkeys(df["status"]))
    ax.legend(handles=[Patch(facecolor=STATUS_COLOURS[s], label=s.replace("_", " ")) for s in statuses],
              loc="lower right", frameon=False)
    fig.tight_layout()
    save_figure(fig, output)


@scientific_plot
def plot_claim_context(claims: pd.DataFrame, output: str | Path) -> None:
    """Plot reported velocity scales while making non-equivalent contexts visible."""
    family_colours = {
        "Design / requirement": PALETTE["grey"],
        "Subsystem calibration": PALETTE["orange"],
        "Commissioning": PALETTE["purple"],
        "On-sky stellar": PALETTE["blue"],
        "Solar time series": PALETTE["sky"],
    }
    ordered = claims.sort_values("value_mps", ascending=False).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 9))
    families = ordered.measurement_context.map(_claim_family)
    colours = [family_colours[value] for value in families]
    ax.barh(ordered.index, ordered.value_mps, color=colours, edgecolor="white", linewidth=0.45)
    ax.set_yticks(ordered.index, ordered.instrument + " · " + ordered.metric.str.replace("_", " "))
    ax.set_xscale("log")
    ax.set_xlabel("Reported velocity scale (m/s, logarithmic axis)")
    ax.set_title("Published numbers describe different experiments — not an instrument ranking")
    ax.grid(axis="x", which="both")
    ax.grid(axis="y", visible=False)
    ax.invert_yaxis()
    ax.legend(
        handles=[
            Patch(facecolor=colour, edgecolor="none", label=family)
            for family, colour in family_colours.items()
        ],
        loc="lower right",
        ncol=2,
    )
    fig.tight_layout()
    save_figure(fig, output)


@scientific_plot
def plot_expres_paired_metrics(metrics: pd.DataFrame, output: str | Path) -> None:
    """Plot only before/after values reported within the same paper and context."""
    fig, axes = plt.subplots(1, len(metrics), figsize=(10, 5), squeeze=False)
    for axis, row in zip(axes[0], metrics.itertuples()):
        values = [row.before_mps, row.after_mps]
        axis.plot([0, 1], values, color=PALETTE["blue"], linewidth=2.4,
                  marker="o", markersize=7, markeredgecolor="white")
        for index, value in enumerate(values):
            offset = (7, 9) if index == 0 else (-7, 9)
            alignment = "left" if index == 0 else "right"
            axis.annotate(f"{value:.2f} m/s", (index, value), xytext=offset,
                          textcoords="offset points", ha=alignment, fontweight="bold")
        axis.set_xticks([0, 1], ["Published baseline", "Published method"])
        axis.set_title(row.label, fontsize=10, wrap=True)
        axis.set_ylim(0, max(values) * 1.25)
        axis.grid(axis="y")
        axis.grid(axis="x", visible=False)
    fig.suptitle("EXPRES before/after results within their original measurement contexts")
    fig.supxlabel("These panels are not comparable instrument rankings")
    fig.tight_layout()
    save_figure(fig, output)


@scientific_plot
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
        colours = [PALETTE["green"] if value < 1 else PALETTE["blue"]
                   for value in frame.value_mps]
        axis.barh(range(len(frame)), frame.value_mps, color=colours,
                  edgecolor="white", linewidth=0.45)
        axis.set_yticks(range(len(frame)), frame.instrument + " · " + frame.metric.str.replace("_", " "))
        axis.set_xscale("log")
        axis.axvline(1.0, color=PALETTE["vermilion"], linestyle="--", linewidth=1.3)
        axis.axvline(0.3, color=PALETTE["purple"], linestyle=":", linewidth=1.5)
        axis.set_title(title)
        axis.grid(axis="x", which="both")
        axis.grid(axis="y", visible=False)
    axes[0].set_xlabel("Reported scale (m/s; metrics remain non-equivalent)")
    axes[1].set_xlabel("Reported scale (m/s; not achieved unless source says so)")
    fig.suptitle("Precision-RV evidence snapshot: measurement context before comparison")
    fig.text(0.5, 0.015, "Dashed: 1 m/s reference · dotted: 0.3 m/s reference", ha="center")
    fig.tight_layout(rect=(0, 0.035, 1, 0.96))
    save_figure(fig, output)


@scientific_plot
def plot_instrument_landscape(
    instruments: pd.DataFrame,
    claims: pd.DataFrame,
    output: str | Path,
) -> None:
    """Combine wavelength coverage and claim context without ranking instruments."""
    columns = [
        "instrument",
        "wave_min_nm",
        "wave_max_nm",
        "spectral_domain",
    ]
    merged = claims.merge(instruments[columns], on="instrument", how="left", validate="many_to_one")
    if merged[["wave_min_nm", "wave_max_nm", "spectral_domain"]].isna().any().any():
        raise ValueError("every performance claim must map to an instrument wavelength range")
    merged["claim_family"] = merged["measurement_context"].map(_claim_family)
    merged["panel"] = np.where(
        merged["claim_family"].isin(["On-sky stellar", "Solar time series"]),
        "On-sky measurements",
        "Requirements, commissioning and subsystem tests",
    )

    marker_by_family = {
        "On-sky stellar": "o",
        "Solar time series": "*",
        "Subsystem calibration": "s",
        "Design / requirement": "^",
        "Commissioning": "D",
    }
    panels = [
        "On-sky measurements",
        "Requirements, commissioning and subsystem tests",
    ]
    label_offsets = {
        "HARPS-N": (-5, -10),
        "SOPHIE+": (4, 8),
        "APF-Levy": (-5, 14),
        "ESPRESSO": (4, -13),
        "EXPRES": (4, -13),
        "CARMENES": (5, -13),
        "IRD": (-5, 9),
        "HPF": (4, 10),
        "PFS": (4, 10),
        "SPIRou": (4, 9),
        "MAROON-X": (4, -13),
        "NEID": (4, -12),
        "NIRPS": (4, -15),
        "HARPS3": (-4, -13),
        "ANDES": (4, 8),
        "G-CLEF": (4, -13),
        ("EXPRES", "Subsystem calibration"): (-5, 9),
        ("G-CLEF", "Design / requirement"): (5, -15),
        ("HARPS3", "Design / requirement"): (-5, -15),
        ("ANDES", "Design / requirement"): (5, 10),
    }

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.4), sharex=True, sharey=True)
    for axis, panel in zip(axes, panels):
        frame = merged[merged["panel"].eq(panel)].copy()
        for row in frame.itertuples(index=False):
            colour = BAND_COLOURS[row.spectral_domain]
            midpoint = math.sqrt(row.wave_min_nm * row.wave_max_nm)
            axis.plot(
                [row.wave_min_nm, row.wave_max_nm],
                [row.value_mps, row.value_mps],
                color=colour,
                linewidth=2.6,
                alpha=0.78,
                solid_capstyle="round",
                zorder=2,
            )
            axis.scatter(
                midpoint,
                row.value_mps,
                marker=marker_by_family[row.claim_family],
                s=58 if row.claim_family != "Solar time series" else 86,
                color=colour,
                edgecolor="white",
                linewidth=0.8,
                zorder=3,
            )
            dx, dy = label_offsets.get(
                (row.instrument, row.claim_family),
                label_offsets.get(row.instrument, (4, 6)),
            )
            axis.annotate(
                row.instrument,
                (midpoint, row.value_mps),
                xytext=(dx, dy),
                textcoords="offset points",
                ha="right" if dx < 0 else "left",
                va="bottom" if dy >= 0 else "top",
                color=INK,
                fontsize=7.2,
                fontweight="bold",
            )

        for velocity, label in [(1.0, "1 m/s"), (0.3, "30 cm/s"), (0.1, "10 cm/s")]:
            axis.axhline(velocity, color=MUTED, linewidth=0.75, linestyle=":", zorder=0)
            axis.text(
                5200,
                velocity * 1.04,
                label,
                ha="right",
                va="bottom",
                color=MUTED,
                fontsize=7,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.8, "alpha": 0.85},
            )
        axis.set_title(panel)
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlim(320, 6000)
        axis.set_ylim(0.065, 16)
        axis.set_xlabel("Nominal wavelength coverage (nm; logarithmic axis)")
        axis.grid(which="major")
        axis.grid(which="minor", alpha=0.3)

    axes[0].set_ylabel("Reported velocity scale (m/s; logarithmic axis)")
    band_handles = [
        Patch(facecolor=colour, edgecolor="none", label=band.replace("_", " "))
        for band, colour in BAND_COLOURS.items()
    ]
    family_handles = [
        plt.Line2D(
            [0],
            [0],
            color=INK,
            marker=marker,
            linestyle="none",
            markersize=6,
            label=family,
        )
        for family, marker in marker_by_family.items()
    ]
    fig.legend(
        handles=band_handles + family_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.94),
        ncol=4,
        columnspacing=1.3,
        handletextpad=0.5,
    )
    fig.suptitle("The EPRV landscape: wavelength grasp and published velocity scales", y=0.995)
    fig.text(
        0.5,
        0.012,
        "Horizontal segments show nominal coverage. Points retain their source context; unlike metrics are not a performance ranking.",
        ha="center",
        color=MUTED,
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.045, 1, 0.88), w_pad=2.0)
    save_figure(fig, output)


@scientific_plot
def plot_keplerian_detectability(scenarios: pd.DataFrame, output: str | Path) -> None:
    """Plot ideal circular-orbit semi-amplitudes from explicit committed assumptions."""
    gravitational_constant = 6.67430e-11
    earth_mass_kg = 5.9722e24
    solar_mass_kg = 1.98847e30
    day_seconds = 86400.0
    periods = [10 ** (-0.3 + index * (3.3 / 179)) for index in range(180)]
    fig, ax = plt.subplots(figsize=(11, 7))
    palette = [INK, PALETTE["blue"], PALETTE["vermilion"], PALETTE["orange"]]
    for colour, row in zip(palette, scenarios.itertuples()):
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
        ax.axhline(value, color=MUTED, linewidth=0.9, linestyle=":" )
        ax.text(1100, value * 1.05, label, ha="right", va="bottom", fontsize=9,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85})
    earth_period = 365.25
    earth_curve = np.asarray([
        ((2 * math.pi * gravitational_constant / (earth_period * day_seconds)) ** (1 / 3)
         * earth_mass_kg / ((solar_mass_kg + earth_mass_kg) ** (2 / 3)))
    ])
    ax.scatter([earth_period], earth_curve, marker="o", s=42, color=PALETTE["green"],
               edgecolor="white", linewidth=0.8, zorder=5)
    ax.annotate("Earth–Sun analogue\nK ≈ 0.089 m/s", (earth_period, earth_curve[0]),
                xytext=(-12, 25), textcoords="offset points", ha="right", va="bottom",
                color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(periods), max(periods))
    ax.set_xlabel("Orbital period, P (days)")
    ax.set_ylabel("Ideal Keplerian semi-amplitude, K (m/s)")
    ax.set_title("Why sub-m/s radial velocities matter")
    ax.grid(which="both")
    ax.legend(frameon=False, loc="lower left")
    fig.text(0.5, 0.01, "Circular, edge-on examples; stellar variability, cadence and instrument systematics are not included.", ha="center")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    save_figure(fig, output)
