import traceback
import praw
import config
from scan import scan


def start():
    print("Starting main")

    reddit = praw.Reddit(
        client_id=config.CLIENT["ID"],
        client_secret=config.CLIENT["SECRET"],
        user_agent=config.USER_AGENT,
        username=config.USERNAME,
        password=config.PASSWORD)

    try:
        scan(reddit.subreddit(config.SUBREDDIT))
    except Exception as e:
        # This should never happen,
        # because it breaks the infinite subreddit monitoring
        # provided by subreddit.stream.submissions()
        print("Exception occurred while scanning. This should never happen!")
        traceback.print_exc()


if __name__ == "__main__":
    start()
