"""
cli.py — Command-line interface for phi-scaling-validator (P38).

Commands
--------
phi-validate run       Run all Φ^(1/3) validation analyses
phi-validate report    Print detailed per-domain report
phi-validate zenodo    Print Zenodo metadata record
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from .phi_constants import PHI, PHI_CUBEROOT, V_RIG
from .system import PhiScalingValidator

app = typer.Typer(
    name="phi-validate",
    help="Package 38 — Φ^(1/3) Universal Scaling Validator (GenesisAeon)",
    no_args_is_help=True,
)
console = Console()


@app.command()
def run(
    packages: str = typer.Option("17-37", help="Package range e.g. '17-37'"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
) -> None:
    """Run all Φ^(1/3) validation analyses across GenesisAeon packages."""
    validator = PhiScalingValidator()
    result = validator.run_cycle()

    if json_output:
        typer.echo(json.dumps(result, indent=2))
        return

    console.print(f"\n[bold cyan]Φ^(1/3) Universal Scaling Validator — P38[/bold cyan]")
    console.print(f"Φ^(1/3) = {PHI_CUBEROOT:.8f}   v_RIG = {V_RIG:.2f} km/s\n")

    table = Table(title="Validation Summary")
    table.add_column("Domain", style="cyan")
    table.add_column("Mean ratio", justify="right")
    table.add_column("p-value", justify="right")
    table.add_column("Confirmed", justify="center")

    for domain, key in [("CREP Spectrum", "crep"), ("Beta-Clusters", "beta"), ("Q4 Landscape", "q4"), ("EML Trees", "eml")]:
        r = result[key]
        confirmed_str = "[green]YES[/green]" if r["confirmed"] else "[red]NO[/red]"
        table.add_row(domain, f"{r['mean_ratio']:.5f}", f"{r['p_value']:.4f}", confirmed_str)

    console.print(table)
    score = result["universality_score"]
    console.print(f"\nUniversality score: [bold]{score:.0%}[/bold] of tested domains\n")


@app.command()
def report() -> None:
    """Print detailed per-domain Φ^(1/3) report."""
    validator = PhiScalingValidator()
    validator.run_cycle()
    occ = validator.phi_occurrences()

    for domain, data in occ.items():
        console.rule(f"[bold]{domain}[/bold]")
        console.print(data.get("note", ""))
        console.print()


@app.command()
def zenodo() -> None:
    """Print Zenodo metadata record for this package."""
    validator = PhiScalingValidator()
    record = validator.to_zenodo_record()
    typer.echo(json.dumps(record, indent=2))
