from pathlib import Path
import re
import sqlite3
import time

from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm
import requests

from paper_glancer.paper import Paper
from .open_review import OpenReviewStub


def _init_2022(db_dir: Path):
    paper_id_pattern = re.compile("maincard_(.*)")
    openreview_id_pattern = re.compile(".*id=(.*)")

    logger.info("Downloading the web page ...")
    response = requests.get("https://nips.cc/Conferences/2022/Schedule?type=Poster")
    logger.success("Web page downloaded.")
    soup = BeautifulSoup(response.text, "html.parser")

    paper_cards = soup.find_all(
        lambda x: x.has_attr("id") and x["id"].startswith("maincard_"))

    db_path = Path(db_dir, "neurips_2022.db")
    db_path.unlink(missing_ok=True)
    conn = sqlite3.connect(db_path)
    Paper.make_sqlite_table(conn)

    logger.info("Going through a list of {} papers ...", len(paper_cards))
    stub = OpenReviewStub()
    for paper_card in tqdm(paper_cards, mininterval=0, miniter=1):
        m = paper_id_pattern.match(paper_card["id"])
        if m is None:
            logger.warning("Cannot parse paper id from {}, skipping", paper_card["id"])
            continue
        paper_id = m.groups()[0]

        response = requests.get(
            f"https://nips.cc/Conferences/2022/Schedule?showEvent={paper_id}")
        if response.status_code != 200:
            logger.warning("Failed to fetch web page for paper with ID = {}", paper_id)
            continue

        psoup = BeautifulSoup(response.text, "html.parser")
        title = psoup.find_all(class_="maincardBody")[0].contents[0]
        
        try: 
            openreview_url = psoup.find_all(title="OpenReview")[0]["href"]
        except Exception:
            logger.warning("Cannot find openreview url for the paper {}", title)
            continue
        m = openreview_id_pattern.match(openreview_url)
        assert m is not None
        try:
            attributes = stub.get_paper_attributes(m.groups()[0])
        except Exception as e:
            logger.warning("Failed to fetch from open review for the paper {}", title)
            continue
        attributes.update({
            "year": 2022,
            "conference": "NeurIPS",
        })
        paper = Paper(**attributes)
        with conn:
            paper.insert_to_sqlite_table(conn)
        time.sleep(0.1)

def init(db_dir: Path, year: int = 2022):
    if year == 2022:
        _init_2022(db_dir)
