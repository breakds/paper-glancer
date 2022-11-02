from pathlib import Path

from loguru import logger
import click

from .impl import neurips


@click.group()
def app():
    pass


@app.command()
@click.option("-c", "--conference", type=str, default="neurips2022")
@click.option("--db", type=click.Path(exists=True), default="/home/breakds/tmp")
def init(conference: str, db: Path):
    if conference == "neurips2022":
        neurips.init(db, year=2022)


if __name__ == "__main__":
    app()
