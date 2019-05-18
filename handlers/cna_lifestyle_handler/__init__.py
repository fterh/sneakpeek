"""Handler for CNA Lifestyle."""

import json
import requests

from bs4 import BeautifulSoup

from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError

class CNAlifestyleHandler(AbstractBaseHandler):
    """Handler for CNA Lifestyle."""

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        article_info = soup.find("meta", {"name":"cXenseParse:mdc-targeturl"})["content"].split('/')
        category_id = article_info[1]
        article_id = article_info[2]

        CNALIFESTYLE_API_URL = (
            f"https://cnalifestyle.channelnewsasia.com/graphql?query=query"
            f"%20article(%24articleId%3A%20String!%2C%20%24categoryId%3A%"
            f"20String!)%20%7B%0A%20%20article(articleId%3A%20%24articleId%2C"
            f"%20categoryId%3A%20%24categoryId)%20%7B%0A%20%20%20%20id%0A"
            f"%20%20%20%20title%0A%20%20%20%20metaTitle%0A%20%20%20%20image%0A"
            f"%20%20%20%20imageWidth%0A%20%20%20%20imageHeight%0A"
            f"%20%20%20%20category%0A%20%20%20%20date%0A%20%20%20%20sharing%0A"
            f"%20%20%20%20exclusive%0A%20%20%20%20link%0A"
            f"%20%20%20%20hasSubjectTaxonomy%0A%20%20%20%20currentContext%20"
            f"%7B%0A%20%20%20%20%20%20title%0A%20%20%20%20%20%20link%0A"
            f"%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A"
            f"%20%20%20%20author%20%7B%0A%20%20%20%20%20%20title%0A"
            f"%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A"
            f"%20%20%20%20contexts%20%7B%0A%20%20%20%20%20%20title%0A"
            f"%20%20%20%20%20%20link%0A%20%20%20%20%20%20__typename%0A"
            f"%20%20%20%20%7D%0A%20%20%20%20defaultPhoto%20%7B%0A"
            f"%20%20%20%20%20%20link%0A%20%20%20%20%20%20__typename%0A"
            f"%20%20%20%20%7D%0A%20%20%20%20photos%20%7B%0A"
            f"%20%20%20%20%20%20teaserText%0A%20%20%20%20%20%20detailText%0A"
            f"%20%20%20%20%20%20photo%20%7B%0A%20%20%20%20%20%20%20%20link%0A"
            f"%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A"
            f"%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A"
            f"%20%20%20%20video%20%7B%0A%20%20%20%20%20%20id%0A"
            f"%20%20%20%20%20%20ooyalaId%0A%20%20%20%20%20%20duration%0A"
            f"%20%20%20%20%20%20playerId%0A%20%20%20%20%20%20category%0A"
            f"%20%20%20%20%20%20sk%20%7B%0A%20%20%20%20%20%20%20%20name%0A"
            f"%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A"
            f"%20%20%20%20%20%20ner%20%7B%0A%20%20%20%20%20%20%20%20name%0A"
            f"%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A"
            f"%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A"
            f"%20%20%20%20audio%20%7B%0A%20%20%20%20%20%20duration%0A"
            f"%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A"
            f"%20%20%20%20html%0A%20%20%20%20teaserText%0A"
            f"%20%20%20%20contentLength%0A%20%20%20%20postedDate%0A"
            f"%20%20%20%20__typename%0A%20%20%7D%0A%7D%0A"
            f"&operationName=article&variables=%7B%22categoryId%22%3A"
            f"%22{category_id}%22%2C%22articleId%22%3A%22{article_id}%22%7D"
        )

        article = json.loads(requests.get(CNALIFESTYLE_API_URL).content)["data"]["article"]

        title = article["title"]
        body = ""

        article_soup = BeautifulSoup(article["html"], "html.parser")
        for line in article_soup.find_all(cls.is_p_tag_without_figure_or_picture):
            body += line.get_text() + "\n\n"

        return Comment(title, body.strip())

    @classmethod
    def is_p_tag_without_figure_or_picture(cls, tag):
        if tag.name != "p":
            return False

        for descendant in tag.descendants:
            if descendant.name == "figure" or descendant.name == "picture":
                return False

        return True
