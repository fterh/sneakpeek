import os
from dotenv import load_dotenv


load_dotenv()

# Set to "prod" in production, but default to "dev"
ENV = os.getenv("ENV", "dev")

BOT = {
    "VERSION": "0.7.0-beta",
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
