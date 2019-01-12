import config
from database import DatabaseManager, DatabaseActionEnum
from handler import HandlerManager
from comment import format_comment
from qualify import qualify


def scan(subreddit):
    """Scan a Subreddit for new submissions."""
    print("Starting scan")

    for submission in subreddit.new(limit=config.LIMIT):
        print("Operating on submission ID: " + submission.id)

        does_qualify = qualify(submission)

        if does_qualify:
            print("Submission qualifies")

            handler = HandlerManager.get_handler(submission.url)
            comment_raw = handler.handle(submission.url)
            comment_markdown = format_comment(comment_raw)

            if len(comment_markdown) < config.COMMENT_LENGTH_LIMIT:
                try:
                    print("Attempting to post a comment")
                    submission.reply(comment_markdown)
                    print("Comment posting succeeded")
                    print("Attempting to write success to database")
                    DatabaseManager.write_id(submission.id, DatabaseActionEnum.SUCCESS)
                    print("Database write succeeded")
                except Exception as e:
                    print("An error occurred:")
                    print(e)
            else:
                print("Submission is too long to be posted.")
                print("Attempting to write skip to database")
                DatabaseManager.write_id(submission.id, DatabaseActionEnum.SKIP)
                print("Database write succeeded")
        else:
            # If submission does not qualify, write SKIP to database only if it is new.
            print("Submission does not qualify")
            print("Checking if submission is new")
            if DatabaseManager.check_id(submission.id):
                print("Submission already exists in database. Skipping.")
            else:
                print("Attempting to write skip to database")
                DatabaseManager.write_id(submission.id, DatabaseActionEnum.SKIP)
                print("Database write succeeded")
