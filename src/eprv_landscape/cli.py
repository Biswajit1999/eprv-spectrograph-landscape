"""Command-line interface for validation, summaries, and figures."""
from __future__ import annotations

import json
from pathlib import Path

import click
import pandas as pd

from .analysis import (
    claim_context_summary,
    performance_evidence_summary,
    spectral_coverage_summary,
    status_summary,
)
from .data import (
    load_expres_metrics,
    load_expres_papers,
    load_instruments,
    load_performance_claims,
)
from .plots import (
    plot_claim_context,
    plot_expres_paired_metrics,
    plot_keplerian_detectability,
    plot_resolution_coverage,
    plot_state_of_art_evidence,
    plot_wavelength_coverage,
)


@click.group()
def main() -> None:
    """Build the EPRV spectrograph landscape from committed evidence tables."""


@main.command("build")
@click.option("--data", "data_path", default="data/instruments.csv", show_default=True)
@click.option("--out", "out_dir", default="results", show_default=True)
@click.option("--claims", "claims_path", default="data/performance_claims.csv", show_default=True)
def build_cmd(data_path: str, out_dir: str, claims_path: str) -> None:
    df = load_instruments(data_path)
    claims = load_performance_claims(claims_path, df)
    expres_papers = load_expres_papers("data/expres_papers.csv")
    expres_metrics = load_expres_metrics("data/expres_metrics.csv", expres_papers)
    paper_paths = sorted(Path("data").glob("*_papers.csv"))
    selected_source_count = sum(len(pd.read_csv(path)) for path in paper_paths)
    with Path("data/instrument_dossiers.json").open(encoding="utf-8") as source:
        dossier_count = len(json.load(source))
    out = Path(out_dir)
    figures = out / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    status_summary(df).to_csv(out / "status_summary.csv", index=False)
    spectral_coverage_summary(df).to_csv(out / "spectral_coverage_summary.csv", index=False)
    performance_evidence_summary(df).to_csv(out / "performance_evidence_summary.csv", index=False)
    claim_context_summary(claims).to_csv(out / "claim_context_summary.csv", index=False)
    plot_wavelength_coverage(df, figures / "wavelength_coverage.png")
    plot_resolution_coverage(df, figures / "resolution_vs_coverage.png")
    plot_claim_context(claims, figures / "reported_velocity_scales.png")
    plot_expres_paired_metrics(expres_metrics, figures / "expres_published_comparisons.png")
    plot_state_of_art_evidence(claims, figures / "state_of_art_evidence.png")
    scenarios = pd.read_csv("data/detectability_scenarios.csv")
    plot_keplerian_detectability(scenarios, figures / "keplerian_detectability.png")
    manifest = {
        "n_instruments": len(df),
        "n_quantitative_claims": len(claims),
        "n_expres_papers_reviewed": len(expres_papers),
        "n_selected_reading_sources": selected_source_count,
        "n_instrument_dossiers": dossier_count,
        "status_as_of_min": str(df["status_as_of"].min()),
        "status_as_of_max": str(df["status_as_of"].max()),
        "performance_classes": sorted(df["performance_class"].unique()),
        "warning": "Reported performance statements use non-equivalent definitions and are not ranked.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    click.echo(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
