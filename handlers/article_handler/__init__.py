from newspaper import Article
from comment import Comment
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError


class ArticleHandler(AbstractBaseHandler):
    @classmethod
    def handle(cls, url):
        article = Article(url)
        article.download()
        article.parse()

        title = article.title
        body = article.text
        body = body.replace('> Advertisement\n\n', '')
        return Comment(title, body)
