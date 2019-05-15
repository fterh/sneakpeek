"""Handler for Yahoo."""

import requests
from bs4 import BeautifulSoup
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class YahooHandler(AbstractBaseHandler):
    """Handler for Yahoo."""

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("meta", {"property":"og:title"})["content"]
        body = ""
        amp_url = soup.find("link", {"rel":"amphtml"})["href"]
        article_html = requests.get(amp_url).text
        article_soup = BeautifulSoup(article_html, "html.parser")
        for line in article_soup.select("article > div.caas-body > p"):
            body += line.get_text() + "\n\n"

        return Comment(title, body.strip())
