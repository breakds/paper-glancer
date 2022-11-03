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

    @staticmethod
    def make_sqlite_table(conn):
        with conn:
            conn.execute("CREATE TABLE papers(title, authors, year, abstract, keywords, conference, tags, ratings, openreview_url, conclusion)")

    def insert_to_sqlite_table(self, conn):
        conn.execute("INSERT INTO papers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (self.title,
                      str(self.authors),
                      self.year,
                      self.abstract,
                      str(self.keywords),
                      self.conference,
                      str(self.tags),
                      str(self.ratings),
                      self.openreview_url,
                      ""))
