import json
import requests

from bs4 import BeautifulSoup

from comment import Comment
from handlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError


class BusinesstimesHandler(AbstractBaseHandler):
    soup = None
    title = None

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        cls.soup = BeautifulSoup(html, "html.parser")
        cls.title = cls.soup.find("meta", {"name":"cXenseParse:title"})["content"]
        return cls.handlePremium() if cls.isPremiumArticle() else cls.handleNonPremium()

    @classmethod
    def isPremiumArticle(cls):
        elem = cls.soup.select_one("div.subscribe-box.paywall-box")
        return elem is not None

    @classmethod
    def handleNonPremium(cls):
        body = ""
        amp_url = cls.soup.find("link", {"rel":"amphtml"})["href"]
        article_html = requests.get(amp_url).text
        article_soup = BeautifulSoup(article_html, "html.parser")
        for line in article_soup.select("div.article-body > p"):
            body += line.get_text() + "\n\n"

        return Comment(cls.title, body.strip())

    @classmethod
    def handlePremium(cls):
        print(f"Article title: {cls.title}")
        print(f"Businesstimes article is paywall blocked.")
        return None
