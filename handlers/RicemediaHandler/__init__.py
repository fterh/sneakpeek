from comment import Comment
from handlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError

import requests
import re
from bs4 import BeautifulSoup
import textwrap

class RicemediaHandler(AbstractBaseHandler):
    @classmethod
    def handle(cls, url):
      html = requests.get(url).text
      soup = BeautifulSoup(html, 'html.parser')

      #https://stackoverflow.com/a/24618186
      # we only want article text, not inline scripts or inline jss
      for script in soup(["script", "style"]):
          script.extract()

      #Plant markers to denote the start and end of the article
      start_marker='EXTRACT_START'
      end_marker='EXTRACT_END'
      soup.find(name='div', class_='post-date').insert(0, start_marker)
      soup.find(name='span', class_='author-name').append(end_marker)

      unwrapped_body = re.search(f'{start_marker}(.+?){end_marker}', soup.text).group(1)
      article_body = '\n'.join(textwrap.wrap(unwrapped_body,80))
      article_title = soup.find(name='h2', class_='post-title').text

      return Comment(article_title, article_body.replace('\xa0', ' '))
