import os
from dotenv import load_dotenv


load_dotenv()

# Set to "prod" in production, but default to "dev"
ENV = os.getenv("ENV", "dev")

# In minutes
RUN_EVERY = 2

BOT = {
    "VERSION": "0.6.0-beta",
    "REPO_LINK": "https://github.com/fterh/sneakpeek",
    "CONTRIBUTE_LINK": "https://github.com/fterh/sneakpeek"
}

DATABASE = {
    "NAME": "main.db" if ENV == "prod" else (
        "main_test.db" if ENV == "test" else "main_dev.db"),
    "TABLES": {
        "SUBMISSIONS": {
            "NAME": "submissions",
            "ID_NAME": "submission_id",
            "ACTION_NAME": "action",
            "ID_INDEX_NAME": "idx_submission_id"
        }
    }
}

CLIENT = {
    "ID": os.getenv("CLIENT_ID"),
    "SECRET": os.getenv("CLIENT_SECRET")
}

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

USER_AGENT = os.getenv("USER_AGENT")

SUBREDDIT = "singapore" if ENV == "prod" else "rsgretrivr"
LIMIT = 10
COMMENT_LENGTH_LIMIT = 9900
