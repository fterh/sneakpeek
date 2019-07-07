"""Handler for CNA."""

import requests
from bs4 import BeautifulSoup
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class CNAHandler(AbstractBaseHandler):
    """Handler for CNA."""

    @classmethod
    def handle(cls, url):
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "lxml")
        title = soup.find("meta", {"name":"cXenseParse:mdc-title"})["content"]
        body = ""

        for line in soup.select("div.c-rte--article > p, div.c-rte--light > p"):
            body += line.get_text() + "\n\n"

        return Comment(title, body.strip())
