from comment import Comment
from handlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError

import requests
import re
from bs4 import BeautifulSoup
import textwrap
import json

class TodayonlineHandler(AbstractBaseHandler):
    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        articleid = soup.find("meta", {"name":"cXenseParse:recs:articleid"})["content"]
        TODAY_API_URL = f"https://www.todayonline.com/api/v3/article/{articleid}"
        article = json.loads(requests.get(TODAY_API_URL).content)["node"]
        title = article["title"]
        body = BeautifulSoup(article["body"], "html.parser").get_text()
        return Comment(title, body)
