"""Handler for Ricemedia."""

import requests
from bs4 import BeautifulSoup
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class RicemediaHandler(AbstractBaseHandler):
    """Handler for Ricemedia."""

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        # https://stackoverflow.com/a/24618186
        # We only want article text, not figure, inline scripts or inline jss
        for script in soup(["figure", "script", "style"]):
            script.extract()

        # Plant markers to denote the start and end of the article
        start_marker = "EXTRACT_START"
        end_marker = "EXTRACT_END"
        soup.find(name="div", class_="post-date").insert(0, start_marker)
        soup.find(name="span", class_="author-name").append(end_marker)

        article_start = soup.text.index(start_marker) + len(start_marker)
        article_end = soup.text.index(end_marker)

        unwrapped_body = soup.text[article_start:article_end]
        article_body = unwrapped_body.replace("\n", "\n\n")  # Markdown requires 2 \n to # create a new paragraph
        article_title = soup.find(name="h2", class_="post-title").text

        return Comment(article_title, article_body.replace("\xa0", " "))
