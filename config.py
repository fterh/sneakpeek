import logging
import os
import sys
import yaml
from dotenv import load_dotenv


load_dotenv()

# Logging configuration
LOGGING = {
    "LEVEL": logging.DEBUG,
    "HANDLER": logging.StreamHandler(sys.stdout)  # Log to stdout (see: https://12factor.net/logs)
}


class BotConfig:
    def __init__(self):
        load_dotenv()
        self.client_id: str = os.getenv('CLIENT_ID')
        self.client_secret: str = os.getenv('CLIENT_SECRET')
        self.username: str = os.getenv('USERNAME')
        self.password: str = os.getenv('PASSWORD')
        self.user_agent: str = os.getenv('USER_AGENT')
        self.comment_length_limit: int = 9900

        # Read subreddit from environment variable; warn and default to /r/all if not set
        self.subreddit: str = os.getenv('SUBREDDIT')
        if self.subreddit is None:
            logging.warning('Environment variable `SUBREDDIT` is not set; defaulting to `all`')
            self.subreddit: str = 'all'

        # load details about bot
        with open('about.yaml', 'r') as f:
            about = yaml.safe_load(f)
        if about is None:
            logging.error('Couldn\'t load \'about.yaml\'')
        self.version = about.get('version')
        self.repo = about.get('repo')


# This is a shitty singleton, but it gets the job done!
# Always import bot_config instead of BotConfig
bot_config = BotConfig()
