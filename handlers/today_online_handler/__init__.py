"""Handler for Today Online."""

import json
import requests
from bs4 import BeautifulSoup
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class TodayonlineHandler(AbstractBaseHandler):
    """Handler for Today Online."""

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        article_id = soup.find("meta", {"name":"cXenseParse:recs:articleid"})["content"]
        TODAY_API_URL = f"https://www.todayonline.com/api/v3/article/{article_id}"
        article = json.loads(requests.get(TODAY_API_URL).content)["node"]
        title = article["title"]
        body = BeautifulSoup(article["body"], "html.parser").get_text()
        body = body.replace("\n", "\n\n")  # Markdown requires 2 \n to create a new paragraph
        return Comment(title, body)
