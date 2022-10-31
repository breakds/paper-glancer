from pathlib import Path
from bs4 import BeautifulSoup

from loguru import logger
import requests


def init_neurips_2022(db_dir: Path):
    response = requests.get("https://nips.cc/Conferences/2022/Schedule?type=Poster")
    soup = BeautifulSoup(response.text, "html.parser")

    # 1. Find the main content
    paper_cards = soup.find_all(
        lambda x: x.has_attr("id") and x["id"].startswith("maincard_"))

    print(len(paper_cards))
