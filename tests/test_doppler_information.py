from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from eprv_landscape.doppler_information import (
    make_line_ensemble,
    photon_limit_mps,
    run_information_experiment,
    simulate_linearized_recovery,
    synthetic_spectrum,
    velocity_grid,
)


def test_photon_limit_has_inverse_square_root_scaling():
    grid = velocity_grid()
    lines = make_line_ensemble()
    low = synthetic_spectrum(grid, lines, 100_000, 2.5, 20_000)
    high = synthetic_spectrum(grid, lines, 100_000, 2.5, 80_000)
    ratio = photon_limit_mps(low, grid) / photon_limit_mps(high, grid)
    assert ratio == pytest.approx(2.0, rel=2e-4)


def test_broader_lines_contain_less_local_doppler_information():
    grid = velocity_grid()
    lines = make_line_ensemble()
    narrow = synthetic_spectrum(grid, lines, 100_000, 1.0, 50_000)
    broad = synthetic_spectrum(grid, lines, 100_000, 5.0, 50_000)
    assert photon_limit_mps(narrow, grid) < photon_limit_mps(broad, grid)


def test_resolution_gain_diminishes_for_broad_lines():
    grid = velocity_grid()
    lines = make_line_ensemble()
    low = synthetic_spectrum(grid, lines, 100_000, 5.0, 50_000)
    high = synthetic_spectrum(grid, lines, 150_000, 5.0, 50_000)
    improvement = 1 - photon_limit_mps(high, grid) / photon_limit_mps(low, grid)
    assert 0 < improvement < 0.10


def test_injection_recovery_matches_information_bound():
    grid = velocity_grid()
    expected = synthetic_spectrum(grid, make_line_ensemble(), 100_000, 2.5, 50_000)
    result = simulate_linearized_recovery(expected, grid, 1500, 10.0, seed=11)
    relative_error = abs(result["empirical_sigma_mps"] / result["predicted_sigma_mps"] - 1)
    assert relative_error < 0.08
    assert abs(result["bias_mps"]) < 0.08 * result["predicted_sigma_mps"]
    assert 0.64 < result["coverage_1sigma"] < 0.72


def test_committed_information_scenarios_are_reproducible(tmp_path):
    output = tmp_path / "information.csv"
    frame = run_information_experiment("data/information_experiment_scenarios.csv", output)
    assert output.exists()
    assert len(frame) == 15
    assert frame["scenario_id"].is_unique
    assert np.isfinite(frame["photon_limit_mps"]).all()
    assert len(frame.dropna(subset=["mc_empirical_sigma_mps"])) == 4
    roundtrip = pd.read_csv(output)
    assert len(roundtrip) == len(frame)


def test_website_publishes_exact_generated_information_assets():
    result_csv = Path("results/doppler_information_experiment.csv")
    public_csv = Path("website/public/data/doppler_information_experiment.csv")
    result_figure = Path("results/figures/doppler_information_experiment.png")
    public_figure = Path("website/public/figures/doppler_information_experiment.png")
    assert public_csv.read_bytes() == result_csv.read_bytes()
    assert public_figure.read_bytes() == result_figure.read_bytes()

    html = Path("website/index.html").read_text(encoding="utf-8")
    assert "Absolute values are not achieved precision" in html
    assert "doppler_information_experiment.csv" in html

    result_figures = Path("results/figures")
    public_figures = Path("website/public/figures")
    for result in result_figures.glob("*.png"):
        assert (public_figures / result.name).read_bytes() == result.read_bytes()


def test_documented_resolution_gains_match_generated_results():
    results = pd.read_csv("results/doppler_information_experiment.csv")
    study = Path("docs/DOPPLER_INFORMATION_STUDY.md").read_text(encoding="utf-8")
    expected = {1.0: "37.1%", 2.5: "11.1%", 5.0: "2.48%"}
    for width, rendered in expected.items():
        subset = results[results["intrinsic_sigma_kms"].eq(width)].set_index(
            "resolving_power"
        )
        improvement = 100 * (
            1 - subset.loc[150000, "photon_limit_mps"] / subset.loc[100000, "photon_limit_mps"]
        )
        decimals = 2 if width == 5.0 else 1
        assert f"{improvement:.{decimals}f}%" == rendered
        assert rendered in study
