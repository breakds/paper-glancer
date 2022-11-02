from pathlib import Path
import re

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
    logger.info("Web page downloaded. Parsing ...")
    soup = BeautifulSoup(response.text, "html.parser")

    paper_cards = soup.find_all(
        lambda x: x.has_attr("id") and x["id"].startswith("maincard_"))

    papers = []
    logger.info("Going through a list of {} papers ...", len(paper_cards))
    stub = OpenReviewStub()
    for paper_card in tqdm(paper_cards):
        m = paper_id_pattern.match(paper_card["id"])
        if m is None:
            logger.warn("Cannot parse paper id from {}, skipping", paper_card["id"])
            continue
        paper_id = m.groups()[0]

        response = requests.get(
            f"https://nips.cc/Conferences/2022/Schedule?showEvent={paper_id}")
        if response.status_code != 200:
            logger.warn("Failed to fetch web page for paper with ID = {}", paper_id)
            continue

        psoup = BeautifulSoup(response.text, "html.parser")
        openreview_url = psoup.find_all(title="OpenReview")[0]["href"]
        m = openreview_id_pattern.match(openreview_url)
        assert m is not None
        attributes = stub.get_paper_attributes(m.groups()[0])
        attributes.update({
            "year": 2022,
            "conference": "NeurIPS",
        })
        print(attributes)
        papers.append(Paper(**attributes))
        break


def init(db_dir: Path, year: int = 2022):
    if year == 2022:
        _init_2022(db_dir)
