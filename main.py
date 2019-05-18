"""Entry point of the sneakpeek application."""

import logging
import praw
import config
from scan import scan


def setup_logging():
    """Configure project logging options."""
    root = logging.getLogger()
    root.setLevel(config.LOGGING["LEVEL"])

    handler = config.LOGGING["HANDLER"]
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    root.addHandler(handler)


def start():
    """Start the sneakpeek application."""
    logging.info("Starting application")
    logging.info("Instantiating Reddit instance")
    reddit = praw.Reddit(
        client_id=config.CLIENT["ID"],
        client_secret=config.CLIENT["SECRET"],
        user_agent=config.USER_AGENT,
        username=config.USERNAME,
        password=config.PASSWORD)

    try:
        scan(reddit.subreddit(config.SUBREDDIT))
    except Exception as exception:
        # This should never happen,
        # because it breaks the infinite subreddit monitoring
        # provided by subreddit.stream.submissions()
        logging.critical("Exception occurred while scanning. This should never happen.")
        logging.critical(exception)


if __name__ == "__main__":
    setup_logging()
    start()
