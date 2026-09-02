"""Command-line interface for validation, summaries, and figures."""
from __future__ import annotations

import json
from pathlib import Path

import click

from .analysis import (
    claim_context_summary,
    performance_evidence_summary,
    spectral_coverage_summary,
    status_summary,
)
from .data import load_instruments, load_performance_claims
from .plots import plot_claim_context, plot_resolution_coverage, plot_wavelength_coverage


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
    manifest = {
        "n_instruments": len(df),
        "n_quantitative_claims": len(claims),
        "status_as_of_min": str(df["status_as_of"].min()),
        "status_as_of_max": str(df["status_as_of"].max()),
        "performance_classes": sorted(df["performance_class"].unique()),
        "warning": "Reported performance statements use non-equivalent definitions and are not ranked.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    click.echo(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
