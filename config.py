import logging
import os
import sys
from dotenv import load_dotenv


load_dotenv()

# Logging configuration
LOGGING = {
    "LEVEL": logging.DEBUG,
    "HANDLER": logging.StreamHandler(sys.stdout)  # Log to stdout (see: https://12factor.net/logs)
}

BOT = {
    "VERSION": "1.0.2",
    "REPO_LINK": "https://github.com/fterh/sneakpeek",
    "CONTRIBUTE_LINK": "https://github.com/fterh/sneakpeek"
}

CLIENT = {
    "ID": os.getenv("CLIENT_ID"),
    "SECRET": os.getenv("CLIENT_SECRET")
}

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

USER_AGENT = os.getenv("USER_AGENT")

# Read subreddit from environment variable; warn and default to /r/all if not set
SUBREDDIT = os.getenv("SUBREDDIT")
if SUBREDDIT is None:
    logging.warning("Environment variable `SUBREDDIT` is not set; defaulting to `all`")
    SUBREDDIT = "all"

COMMENT_LENGTH_LIMIT = 9900
