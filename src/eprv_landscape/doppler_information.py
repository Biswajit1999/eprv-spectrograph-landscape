"""Controlled photon-limited Doppler-information experiments.

The experiment deliberately operates on a synthetic line ensemble.  It asks
how resolving power and astrophysical line width affect the Cramer-Rao lower
bound when the wavelength grid, photon budget, and line equivalent widths are
held fixed.  It is not an instrument-performance model.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SPEED_OF_LIGHT_KMS = 299_792.458
GAUSSIAN_FWHM_TO_SIGMA = 2.0 * np.sqrt(2.0 * np.log(2.0))


@dataclass(frozen=True)
class SyntheticLine:
    """One absorption line in velocity coordinates.

    ``equivalent_width_kms`` is the area removed from a unit continuum.  The
    area is conserved when instrumental broadening changes.
    """

    center_kms: float
    equivalent_width_kms: float


def velocity_grid(
    minimum_kms: float = -120.0,
    maximum_kms: float = 120.0,
    step_kms: float = 0.05,
) -> np.ndarray:
    """Return an evenly spaced velocity grid with validated bounds."""
    if maximum_kms <= minimum_kms:
        raise ValueError("maximum_kms must exceed minimum_kms")
    if step_kms <= 0:
        raise ValueError("step_kms must be positive")
    count = int(np.floor((maximum_kms - minimum_kms) / step_kms)) + 1
    return minimum_kms + np.arange(count, dtype=float) * step_kms


def make_line_ensemble(
    n_lines: int = 36,
    minimum_kms: float = -108.0,
    maximum_kms: float = 108.0,
    seed: int = 20260918,
) -> tuple[SyntheticLine, ...]:
    """Create a deterministic, separated ensemble with varied equivalent widths."""
    if n_lines < 2:
        raise ValueError("n_lines must be at least two")
    rng = np.random.default_rng(seed)
    spacing = (maximum_kms - minimum_kms) / (n_lines - 1)
    centres = np.linspace(minimum_kms, maximum_kms, n_lines)
    centres += rng.uniform(-0.16 * spacing, 0.16 * spacing, size=n_lines)
    equivalent_widths = rng.uniform(0.20, 0.72, size=n_lines)
    return tuple(
        SyntheticLine(float(center), float(width))
        for center, width in zip(centres, equivalent_widths)
    )


def synthetic_spectrum(
    velocities_kms: np.ndarray,
    lines: tuple[SyntheticLine, ...],
    resolving_power: float,
    intrinsic_sigma_kms: float,
    continuum_photons_per_bin: float,
) -> np.ndarray:
    """Generate expected photo-electrons for a broadened absorption spectrum.

    The Gaussian instrumental width is ``c / R / 2.355``.  Intrinsic and
    instrumental Gaussian widths add in quadrature.  Equivalent width is
    conserved, so the comparison does not reward higher resolution by silently
    deepening lines or changing the photon budget.
    """
    if resolving_power <= 0:
        raise ValueError("resolving_power must be positive")
    if intrinsic_sigma_kms <= 0:
        raise ValueError("intrinsic_sigma_kms must be positive")
    if continuum_photons_per_bin <= 0:
        raise ValueError("continuum_photons_per_bin must be positive")
    if velocities_kms.ndim != 1 or len(velocities_kms) < 3:
        raise ValueError("velocities_kms must be a one-dimensional grid")

    instrumental_sigma = SPEED_OF_LIGHT_KMS / resolving_power / GAUSSIAN_FWHM_TO_SIGMA
    observed_sigma = np.hypot(intrinsic_sigma_kms, instrumental_sigma)
    absorption = np.zeros_like(velocities_kms, dtype=float)
    normalization = np.sqrt(2.0 * np.pi) * observed_sigma
    for line in lines:
        depth = line.equivalent_width_kms / normalization
        offset = (velocities_kms - line.center_kms) / observed_sigma
        absorption += depth * np.exp(-0.5 * offset**2)

    normalized_flux = 1.0 - absorption
    if normalized_flux.min() <= 0:
        raise ValueError("line ensemble produces non-positive flux; reduce line overlap")
    return continuum_photons_per_bin * normalized_flux


def photon_limit_mps(
    expected_counts: np.ndarray,
    velocities_kms: np.ndarray,
    read_noise_e: float = 0.0,
) -> float:
    """Return the local Cramer-Rao photon/read-noise limit in m/s.

    For independent Gaussian/Poisson pixels, the shift information is
    ``sum((d mu / d v)^2 / variance)``.  This is the velocity-coordinate form
    of the spectral-gradient weighting used for Doppler quality factors.
    """
    if read_noise_e < 0:
        raise ValueError("read_noise_e cannot be negative")
    if expected_counts.shape != velocities_kms.shape:
        raise ValueError("expected_counts and velocities_kms must have the same shape")
    if np.any(expected_counts <= 0):
        raise ValueError("expected_counts must be positive")
    velocities_mps = velocities_kms * 1000.0
    derivative = np.gradient(expected_counts, velocities_mps)
    variance = expected_counts + read_noise_e**2
    information = np.sum(derivative**2 / variance)
    if information <= 0 or not np.isfinite(information):
        raise ValueError("spectrum contains no finite Doppler information")
    return float(1.0 / np.sqrt(information))


def simulate_linearized_recovery(
    expected_counts: np.ndarray,
    velocities_kms: np.ndarray,
    n_trials: int,
    injected_sigma_mps: float,
    seed: int,
    read_noise_e: float = 0.0,
    batch_size: int = 100,
) -> dict[str, float]:
    """Validate the local information bound with injected small Doppler shifts.

    A one-step maximum-likelihood estimator is used around the unshifted
    template.  The injected shifts are intentionally much smaller than the line
    width, which is the regime where the local Fisher prediction applies.
    """
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    if injected_sigma_mps <= 0:
        raise ValueError("injected_sigma_mps must be positive")
    rng = np.random.default_rng(seed)
    velocities_mps = velocities_kms * 1000.0
    model_derivative = -np.gradient(expected_counts, velocities_mps)
    variance = expected_counts + read_noise_e**2
    information = float(np.sum(model_derivative**2 / variance))
    predicted_sigma = 1.0 / np.sqrt(information)
    estimates: list[np.ndarray] = []
    truths: list[np.ndarray] = []

    for start in range(0, n_trials, batch_size):
        size = min(batch_size, n_trials - start)
        shifts = rng.normal(0.0, injected_sigma_mps, size=size)
        shifted = np.vstack(
            [
                np.interp(
                    velocities_kms - shift / 1000.0,
                    velocities_kms,
                    expected_counts,
                    left=expected_counts[0],
                    right=expected_counts[-1],
                )
                for shift in shifts
            ]
        )
        observations = rng.poisson(shifted)
        if read_noise_e:
            observations = observations + rng.normal(0.0, read_noise_e, observations.shape)
        score = np.sum((observations - expected_counts) * model_derivative / variance, axis=1)
        estimates.append(score / information)
        truths.append(shifts)

    recovered = np.concatenate(estimates)
    injected = np.concatenate(truths)
    errors = recovered - injected
    standard_error = float(np.std(errors, ddof=1) / np.sqrt(n_trials))
    coverage_standard_error = float(np.sqrt(0.68 * 0.32 / n_trials))
    return {
        "n_trials": float(n_trials),
        "predicted_sigma_mps": float(predicted_sigma),
        "bias_mps": float(np.mean(errors)),
        "empirical_sigma_mps": float(np.std(errors, ddof=1)),
        "empirical_sigma_standard_error_mps": standard_error,
        "coverage_1sigma": float(np.mean(np.abs(errors) <= predicted_sigma)),
        "coverage_standard_error": coverage_standard_error,
    }


def run_information_experiment(
    scenarios_path: str | Path,
    output_path: str | Path,
) -> pd.DataFrame:
    """Run all committed scenarios and write a machine-readable result table."""
    scenarios = pd.read_csv(scenarios_path)
    required = {
        "scenario_id",
        "resolving_power",
        "intrinsic_sigma_kms",
        "continuum_photons_per_bin",
        "read_noise_e",
        "monte_carlo_trials",
        "injected_sigma_mps",
        "seed",
    }
    missing = required - set(scenarios.columns)
    if missing:
        raise ValueError(f"missing information-experiment columns: {sorted(missing)}")
    if scenarios["scenario_id"].duplicated().any():
        raise ValueError("information-experiment scenario identifiers must be unique")

    grid = velocity_grid()
    lines = make_line_ensemble()
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios.itertuples(index=False):
        expected = synthetic_spectrum(
            grid,
            lines,
            float(scenario.resolving_power),
            float(scenario.intrinsic_sigma_kms),
            float(scenario.continuum_photons_per_bin),
        )
        limit = photon_limit_mps(expected, grid, float(scenario.read_noise_e))
        result: dict[str, float | int | str] = {
            "scenario_id": scenario.scenario_id,
            "resolving_power": int(scenario.resolving_power),
            "intrinsic_sigma_kms": float(scenario.intrinsic_sigma_kms),
            "continuum_photons_per_bin": float(scenario.continuum_photons_per_bin),
            "read_noise_e": float(scenario.read_noise_e),
            "photon_limit_mps": limit,
            "monte_carlo_trials": int(scenario.monte_carlo_trials),
            "mc_bias_mps": np.nan,
            "mc_empirical_sigma_mps": np.nan,
            "mc_empirical_sigma_standard_error_mps": np.nan,
            "mc_coverage_1sigma": np.nan,
            "mc_coverage_standard_error": np.nan,
        }
        if int(scenario.monte_carlo_trials) > 0:
            recovery = simulate_linearized_recovery(
                expected,
                grid,
                int(scenario.monte_carlo_trials),
                float(scenario.injected_sigma_mps),
                int(scenario.seed),
                float(scenario.read_noise_e),
            )
            result.update(
                {
                    "mc_bias_mps": recovery["bias_mps"],
                    "mc_empirical_sigma_mps": recovery["empirical_sigma_mps"],
                    "mc_empirical_sigma_standard_error_mps": recovery[
                        "empirical_sigma_standard_error_mps"
                    ],
                    "mc_coverage_1sigma": recovery["coverage_1sigma"],
                    "mc_coverage_standard_error": recovery["coverage_standard_error"],
                }
            )
        rows.append(result)

    frame = pd.DataFrame(rows)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False, float_format="%.8g")
    return frame


def plot_information_experiment(results: pd.DataFrame, output: str | Path) -> None:
    """Plot the simultaneous resolution/broadening sensitivity analysis."""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    markers = {1.0: "o", 2.5: "s", 5.0: "^"}
    colours = {1.0: "#0f766e", 2.5: "#2563eb", 5.0: "#c2410c"}
    for width, frame in results.groupby("intrinsic_sigma_kms"):
        ordered = frame.sort_values("resolving_power")
        ax.plot(
            ordered["resolving_power"],
            ordered["photon_limit_mps"],
            marker=markers[float(width)],
            color=colours[float(width)],
            linewidth=2.2,
            label=f"intrinsic sigma = {width:g} km/s",
        )
        validated = ordered.dropna(subset=["mc_empirical_sigma_mps"])
        if not validated.empty:
            ax.errorbar(
                validated["resolving_power"],
                validated["mc_empirical_sigma_mps"],
                yerr=validated["mc_empirical_sigma_standard_error_mps"],
                fmt="none",
                ecolor=colours[float(width)],
                capsize=3,
                alpha=0.8,
            )
    ax.set_xlabel("Resolving power, R")
    ax.set_ylabel("Idealized local RV uncertainty (m/s)")
    ax.set_title("Photon-limited information depends jointly on resolution and line width")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    fig.text(
        0.5,
        0.01,
        "Fixed synthetic line ensemble and photons per 50 m/s grid bin; no stellar variability, tellurics, calibration drift or throughput model.",
        ha="center",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output, dpi=180)
    plt.close(fig)
