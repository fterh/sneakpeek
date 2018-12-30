from database import DatabaseManager
from handler import HandlerManager


def qualify(submission):
    """
    Check if a submission qualifies to be previewed by the bot.
    Conditions for preview:
    (1) Submission is a link
    (2) Submission has not been previously encountered
    (3) Submission has a Handler
    """
    # Check (1) Submission is a link
    is_link = not submission.is_self

    # Check (2) Submission is new
    is_new = not DatabaseManager.check_id(submission.id)

    # Check (3) Submission has a Handler
    has_handler = HandlerManager.has_handler(submission.url)

    return is_link and is_new and has_handler
