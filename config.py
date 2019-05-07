import logging
import os
import sys
from dotenv import load_dotenv


load_dotenv()

# Set to "prod" in production, but default to "dev"
ENV = os.getenv("ENV", "dev")

# Logging configuration
LOGGING = {
    "LEVEL": logging.DEBUG,
    "HANDLER": logging.StreamHandler(sys.stdout)  # Log to stdout (see: https://12factor.net/logs)
}

BOT = {
    "VERSION": "0.8.0-beta",
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

SUBREDDIT = "singapore" if ENV == "prod" else "rsgretrivr"
COMMENT_LENGTH_LIMIT = 9900
