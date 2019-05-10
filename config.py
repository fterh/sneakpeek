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
    "VERSION": "1.0.0",
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

SUBREDDIT = os.getenv("SUBREDDIT", "all")  # Set subreddit using environmental variables, default to /r/all
COMMENT_LENGTH_LIMIT = 9900
