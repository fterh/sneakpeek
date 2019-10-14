from newspaper import Article
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class MothershipHandler(AbstractBaseHandler):
    @classmethod
    def handle(cls, url):
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        body = article.text
        # replace parsed arguments and trailing ads
        body = body.replace('\nAdvertisement\n', '')
        body = body.partition('Content that keeps Mothership.sg going')

        return Comment(title, body[0])
