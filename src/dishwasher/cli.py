from pathlib import Path

import typer

from dishwasher import __version__
from dishwasher.inspect import inspect_file
from dishwasher.profile import profile_file

app = typer.Typer(help="Clean, standardize and validate tabular data.")


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
    result = inspect_file(path)

    typer.echo(f"File: {result.path}")
    typer.echo("")
    typer.echo(f"Rows: {result.rows}")
    typer.echo(f"Columns: {result.columns}")
    typer.echo("")

    for name, dtype in result.schema.items():
        typer.echo(f"{name:<30} {dtype}")

@app.command()
def profile(path: Path) -> None:
    """Profile a tabular file."""
    result = profile_file(path)

    typer.echo(f"File: {result.path}")
    typer.echo("")
    typer.echo(f"Rows: {result.rows}")
    typer.echo(f"Columns: {result.columns}")
    typer.echo("")
    typer.echo(f"{'Column':<30} {'Type':<15} {'Nulls':>10} {'Unique':>10}")
    typer.echo("-" * 70)

    for column in result.column_profiles:
        typer.echo(
            f"{column.name:<30} "
            f"{column.dtype:<15} "
            f"{column.null_count:>10} "
            f"{column.unique_count:>10}"
        )
