"""Entry point of the sneakpeek application."""

import logging
import praw
from scan import scan
from config import bot_config


def setup_logging():
    """Configure project logging options."""
    root = logging.getLogger()
    root.setLevel(bot_config.logging_level)

    handler = bot_config.logging_handler
    handler.setLevel(bot_config.logging_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    root.addHandler(handler)


def start():
    """Start the sneakpeek application."""
    logging.info("Starting application")
    logging.info("Instantiating Reddit instance")

    reddit = praw.Reddit(
        client_id=bot_config.client_id,
        client_secret=bot_config.client_secret,
        user_agent=bot_config.user_agent,
        username=bot_config.username,
        password=bot_config.password
    )

    try:
        scan(reddit.subreddit(bot_config.subreddit))
    except Exception as exception:
        # This should never happen,
        # because it breaks the infinite subreddit monitoring
        # provided by subreddit.stream.submissions()
        logging.critical("Exception occurred while scanning. This should never happen.")
        logging.critical(exception)


if __name__ == "__main__":
    setup_logging()
    start()
