import typer

from dishwasher import __version__

app = typer.Typer(help="Clean, standardize and validate tabular data.")


@app.callback()
def main() -> None:
    """Dishwasher command line interface."""
    pass


@app.command()
def version() -> None:
    """Show installed version."""
    typer.echo(__version__)
