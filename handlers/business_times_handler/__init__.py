"""Handler for Business Times."""

import requests

from bs4 import BeautifulSoup

from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class BusinesstimesHandler(AbstractBaseHandler):
    """Handler for Business Times."""

    soup = None
    title = None

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        cls.soup = BeautifulSoup(html, "html.parser")
        cls.title = cls.soup.find("meta", {"name":"cXenseParse:title"})["content"]
        return cls.handle_premium() if cls.is_premium_article() else cls.handle_non_premium()

    @classmethod
    def is_premium_article(cls):
        """Check if an article is premium."""
        elem = cls.soup.select_one("div.subscribe-box.paywall-box")
        return elem is not None

    @classmethod
    def handle_non_premium(cls):
        """Handle a non-premium article."""
        body = ""
        amp_url = cls.soup.find("link", {"rel":"amphtml"})["href"]
        article_html = requests.get(amp_url).text
        article_soup = BeautifulSoup(article_html, "html.parser")
        for line in article_soup.select("div.article-body > p"):
            body += line.get_text() + "\n\n"

        return Comment(cls.title, body.strip())

    @classmethod
    def handle_premium(cls):
        """Handle a premium article."""
        print(f"Article title: {cls.title}")
        print(f"Businesstimes article is paywall blocked.")
