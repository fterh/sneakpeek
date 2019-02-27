import json
import requests

from bs4 import BeautifulSoup

from comment import Comment
from handlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError


class TNPHandler(AbstractBaseHandler):
    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("meta", {"property":"og:title"})["content"]
        body = ""
        for line in soup.select("div.body-copy > p, div.body-copy > h2, div.substory h2"):
            body += line.get_text() + "\n\n"

        return Comment(title, body.strip())
