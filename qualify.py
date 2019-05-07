import logging
from handler import HandlerManager


def qualify(submission):
    """
    Check if a submission qualifies to be previewed by the bot.
    Conditions for preview:
    (1) Submission is a link
    (2) Submission has a Handler
    """
    logging.info("Qualifying submission id: {}".format(submission.id))

    # Check (1) Submission is a link
    is_link = not submission.is_self

    # Check (2) Submission has a Handler
    has_handler = HandlerManager.has_handler(submission.url)

    logging.debug("is_link = {}, has_handler = {}".format(is_link, has_handler))

    return is_link and has_handler
