from typing import List

from loguru import logger
import openreview


class OpenReviewStub(object):
    def __init__(self):
        with open("/home/breakds/.config/openreview/config.txt", "r") as f:
            password = f.readline().strip()
        self._client = openreview.Client(
            baseurl="https://api.openreview.net",
            username="breakds@gmail.com",
            password=password)

    def get_paper_attributes(self, id: str) -> dict:
        note = self._client.get_all_notes(id, details="directReplies")[0]
        attributes = {
            "title": note.content["title"],
            "authors": note.content["authors"],
            "abstract": note.content["abstract"],
            "openreview_url": f"https://openreview.net/forum?id={id}",
            "ratings": [],
        }

        for review in note.details["directReplies"]:
            if "content" not in review:
                continue
            if "rating" not in review["content"]:
                continue
            attributes["ratings"].append(float(review["content"]["rating"][0]))

        return attributes
