import time

import praw
import schedule

import config
from database import DatabaseManager
from scan import scan


def start():
    print("Starting main")

    reddit = praw.Reddit(
        client_id=config.CLIENT["ID"],
        client_secret=config.CLIENT["SECRET"],
        user_agent=config.USER_AGENT,
        username=config.USERNAME,
        password=config.PASSWORD)

    scan(reddit.subreddit(config.SUBREDDIT))

    DatabaseManager.disconnect()


schedule.every(config.RUN_EVERY).minutes.do(start)


if __name__ == "__main__":
    start()
    while True:
        schedule.run_pending()
        print("Sleeping")
        time.sleep(1)
