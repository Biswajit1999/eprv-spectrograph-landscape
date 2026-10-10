"""Shared publication-style settings for repository-native scientific figures."""
from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar, cast

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401  # Registers the SciencePlots style sheets.

INK = "#202621"
MUTED = "#62685f"
GRID = "#ded8cc"
PALETTE = {
    "blue": "#236B73",
    "sky": "#6E9E9A",
    "green": "#5F7250",
    "orange": "#B57B2A",
    "vermilion": "#A64B36",
    "purple": "#76658A",
    "grey": "#7A7D75",
    "navy": INK,
}

PlotFunction = TypeVar("PlotFunction", bound=Callable[..., Any])


def scientific_plot(function: PlotFunction) -> PlotFunction:
    """Run a plotting function with a consistent SciencePlots/no-LaTeX theme."""

    @wraps(function)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        with plt.style.context(["science", "no-latex"]), plt.rc_context(
            {
                "axes.edgecolor": INK,
                "axes.labelcolor": INK,
                "axes.titlecolor": INK,
                "axes.titlesize": 11,
                "axes.titleweight": "normal",
                "axes.labelsize": 10,
                "axes.linewidth": 0.8,
                "axes.grid": True,
                "axes.axisbelow": True,
                "grid.color": GRID,
                "grid.linewidth": 0.55,
                "grid.alpha": 0.75,
                "font.family": "DejaVu Sans",
                "font.size": 9.5,
                "legend.fontsize": 8,
                "legend.frameon": False,
                "lines.linewidth": 2.0,
                "savefig.dpi": 300,
                "savefig.facecolor": "white",
                "savefig.bbox": "tight",
                "xtick.color": MUTED,
                "ytick.color": MUTED,
                "xtick.labelsize": 8,
                "ytick.labelsize": 8,
            }
        ):
            return function(*args, **kwargs)

    return cast(PlotFunction, wrapped)


def save_figure(fig: plt.Figure, output: str | Path) -> None:
    """Write a deterministic high-resolution PNG and close its Matplotlib figure."""
    fig.savefig(
        output,
        dpi=300,
        facecolor="white",
        bbox_inches="tight",
        metadata={"Software": "eprv-landscape + Matplotlib + SciencePlots"},
    )
    plt.close(fig)
