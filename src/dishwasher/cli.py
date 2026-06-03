from pathlib import Path

import typer

from dishwasher import __version__
from dishwasher.io import read_table

app = typer.Typer(
    help="Clean, standardize and validate tabular data."
)


@app.callback()
def main() -> None:
    """Dishwasher command line interface."""
    pass


@app.command()
def version() -> None:
    """Show installed version."""
    typer.echo(__version__)


@app.command()
def inspect(path: Path) -> None:
    """Inspect a tabular file."""

    df = read_table(path)

    typer.echo(f"File: {path}")
    typer.echo("")
    typer.echo(f"Rows: {df.height}")
    typer.echo(f"Columns: {df.width}")
    typer.echo("")

    for name, dtype in df.schema.items():
        typer.echo(f"{name:<30} {dtype}")
