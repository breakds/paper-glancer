from typing import List

from loguru import logger
from bs4 import BeautifulSoup
import requests


def _is_rating_field(x):
    if


def fetch_scores(url: str) -> List[float]:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    response = requests.get(url)
    if response.status_code != 200:
        logger.warn("Failed to fetch open review page at {}", url)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
