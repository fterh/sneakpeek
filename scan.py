import traceback

import config
import sys
from handler import HandlerManager
from comment import format_comment
from qualify import qualify


def scan(subreddit):
    """Scan a Subreddit for new submissions."""
    print("Starting scan")

    for submission in subreddit.stream.submissions(skip_existing=True):
        print("Operating on submission ID: " + submission.id)

        does_qualify = qualify(submission)

        if does_qualify:
            print("Submission qualifies")

            handler = HandlerManager.get_handler(submission.url)

            comment_raw = None
            try:
                comment_raw = handler.handle(submission.url)
            except Exception as e:
                print(f"Exception occurred while handling {submission.url}")
                traceback.print_exc()

            if comment_raw is None:
                skip(submission)
                return
            comment_markdown = format_comment(comment_raw)

            if len(comment_markdown) < config.COMMENT_LENGTH_LIMIT:
                try:
                    print("Attempting to post a comment")
                    submission.reply(comment_markdown)
                    print("Comment posting succeeded")
                except Exception as e:
                    print("An error occurred:")
                    print(e)
            else:
                print("Submission is too long to be posted.")
        else:
            skip(submission)

        # Flush stdout buffer
        sys.stdout.flush()

def skip(submission):
    # If submission does not qualify, write SKIP to database only if it is new.
    print("Submission does not qualify")
