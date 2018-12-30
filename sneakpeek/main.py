import praw

import config
from database import DatabaseManager
from scan import scan


if __name__ == "__main__":
    print("Starting main")

    reddit = praw.Reddit(
        client_id=config.CLIENT["ID"],
        client_secret=config.CLIENT["SECRET"],
        user_agent=config.USER_AGENT,
        username=config.USERNAME,
        password=config.PASSWORD)

    scan(reddit.subreddit(config.SUBREDDIT))

    DatabaseManager.disconnect()
