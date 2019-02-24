import tldextract

from collections import defaultdict

from handlers.ArticleHandler import ArticleHandler
from handlers.RicemediaHandler import RicemediaHandler
from handlers.STHandler import STHandler
from handlers.TodayonlineHandler import TodayonlineHandler


class HandlerManager:
    """
    Manage Handlers and map subdomains and domain names to Handlers.
    """
    handlers = {
        "channelnewsasia.com": defaultdict(
            lambda: ArticleHandler # Default Handler for all subdomains (unless specify) for channelnewsasia.com
        ),
        "mothership.sg": defaultdict(
            lambda: ArticleHandler
        ),
        "ricemedia.co": defaultdict(
            lambda: RicemediaHandler
        ),
        "straitstimes.com": defaultdict(
            lambda: STHandler
        ),
        "todayonline.com": defaultdict(
            lambda: TodayonlineHandler
        ),
        "zula.sg": defaultdict(
            lambda: ArticleHandler
        )
    }

    @classmethod
    def extract_hostname(cls, url):
        """Extract subdomain and domain name from URL."""
        url_extract = tldextract.extract(url)
        domains = {
            "subdomain": url_extract.subdomain,
            "domain_name": url_extract.domain + "." + url_extract.suffix
        }
        return domains

    @classmethod
    def has_handler(cls, url):
        """Check if a submission URL has an appropriate Handler."""
        domains = cls.extract_hostname(url)
        return domains["domain_name"] in cls.handlers

    @classmethod
    def get_handler(cls, url):
        """
        Return the Handler corresponding to a subdomain and domain name.
        Will return the default domain Handler if subdomain Handler do not exist.
        Raise ValueError if no domain Handler exists.
        """
        if not cls.has_handler(url):
            raise ValueError("Domain name {} has no Handler".format(url))
        domains = cls.extract_hostname(url)
        return cls.handlers[domains["domain_name"]][domains["subdomain"]]