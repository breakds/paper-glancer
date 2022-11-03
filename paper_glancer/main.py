from pathlib import Path
import sqlite3

from loguru import logger
import click

from .impl import neurips


@click.group()
def app():
    pass


@app.command()
@click.option("-c", "--conference", type=str, default="neurips2022")
@click.option("--db", type=click.Path(exists=True),
              default="/home/breakds/dataset/paper_glancer")
def init(conference: str, db: Path):
    if conference == "neurips2022":
        neurips.init(db, year=2022)


@app.command()
@click.option("-c", "--conference", type=str, default="neurips2022")
@click.option("--db", type=click.Path(exists=True),
              default="/home/breakds/dataset/paper_glancer")
def blog(conference: str, db: Path):
    path = None
    
    if conference == "neurips2022":
        path = neurips.get_db(db, 2022)

    if path is None:
        logger.warning("Cannot find the database for conference {}", conference)
        return

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    result = cur.execute("SELECT title, authors, ratings, openreview_url, abstract "
                         "FROM papers")

    def _to_list(x, transforms=[]):
        y = x[1:-1].split(", ")
        for t in transforms:
            y = [t(e) for e in y]
        return y

    i = 0
    while (entry := result.fetchone()) is not None:
        i = i + 1
        title, authors, ratings, openreview_url, abstract = entry
        authors = _to_list(authors, [lambda x: x[1:-1]])
        ratings = _to_list(ratings, [float, int])
        print(f"#### {i}. {title}")
        print(f"* {', '.join(authors)}")
        print(f"* **Review**: {'/'.join([f'{x}✩' for x in ratings])} "
              f" [openreview]({openreview_url})")
        print()
        print("**Abstract**:", abstract)
        print("\n---\n")


if __name__ == "__main__":
    app()
