from typing import List, NamedTuple


class Paper(NamedTuple):
    title: str = ""
    authors: List[str] = []
    year: int = 5000
    abstract: str = ""
    keywords: List[str] = []
    conference: str = ""
    tags: List[str] = []
    ratings: List[float] = []
    openreview_url: str = ""
