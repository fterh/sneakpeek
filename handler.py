import tldextract

from handlers.ArticleHandler import ArticleHandler


class HandlerManager:
    """
    Manage Handlers and map domain names to Handlers.
    """
    handlers = {
        "channelnewsasia.com": ArticleHandler,
        "mothership.sg": ArticleHandler,
        "straitstimes.com": ArticleHandler,
        "todayonline.com": ArticleHandler,
        "zula.sg": ArticleHandler
    }

    @classmethod
    def extract_hostname(cls, url):
        """Extract hostname from URL."""
        url_extract = tldextract.extract(url)
        return url_extract.domain + "." + url_extract.suffix

    @classmethod
    def has_handler(cls, url):
        """Check if a submission URL has an appropriate Handler."""
        domain_name = cls.extract_hostname(url)
        return domain_name in cls.handlers

    @classmethod
    def get_handler(cls, url):
        """
        Return the Handler corresponding to a domain name.
        Raise ValueError if no such Handler exists.
        """
        if not cls.has_handler(url):
            raise ValueError("Domain name {} has no Handler".format(url))
        domain_name = cls.extract_hostname(url)
        return cls.handlers[domain_name]
