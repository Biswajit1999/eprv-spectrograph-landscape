"""Shared publication-style settings for repository-native scientific figures."""
from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar, cast

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401  # Registers the SciencePlots style sheets.

INK = "#102a43"
MUTED = "#627d98"
GRID = "#d9e2ec"
PALETTE = {
    "blue": "#0072B2",
    "sky": "#56B4E9",
    "green": "#009E73",
    "orange": "#E69F00",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "grey": "#7B8794",
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
                "axes.titlesize": 13,
                "axes.titleweight": "bold",
                "axes.labelsize": 10,
                "axes.linewidth": 0.8,
                "axes.grid": True,
                "axes.axisbelow": True,
                "grid.color": GRID,
                "grid.linewidth": 0.55,
                "grid.alpha": 0.75,
                "font.family": "DejaVu Sans",
                "font.size": 9,
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
