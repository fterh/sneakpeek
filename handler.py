import tldextract

from handlers.ArticleHandler import ArticleHandler
from handlers.RicemediaHandler import RicemediaHandler
from handlers.TodayonlineHandler import TodayonlineHandler


class HandlerManager:
    """
    Manage Handlers and map domain names to Handlers.
    """
    handlers = {
        "channelnewsasia.com": ArticleHandler,
        "mothership.sg": ArticleHandler,
        "ricemedia.co": RicemediaHandler,
        # "straitstimes.com": ArticleHandler,  # Temporarily remove support until premium article detection
        "todayonline.com": TodayonlineHandler,
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
