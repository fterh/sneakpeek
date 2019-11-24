"""Monitor a Subreddit for new submissions."""

import logging
import config
from handler import HandlerManager
from qualify import qualify
from config import bot_config


def scan(subreddit):
    """Scan a Subreddit for new submissions."""
    logging.info("Starting scan")

    for submission in subreddit.stream.submissions(skip_existing=True):
        logging.info("Operating on submission")
        logging.debug("Submission ID = %s, title = %s",
                      submission.id,
                      submission.title)

        does_qualify = qualify(submission)

        if not does_qualify:
            logging.info("Comment does not qualify; skipping comment")
            continue

        logging.info("Submission qualifies")

        handler = None
        try:
            logging.info("Attempting to get article handler")
            handler = HandlerManager.get_handler(submission.url)
            logging.info("Article handler = %s",
                         handler)
        except Exception as exception:
            logging.error("""
                            An error occurred while getting article handler. This should never happen.
                            """)
            logging.error("Exception = %s", exception)
            logging.info("Skipping current submission")
            continue

        comment = None
        try:
            logging.info("Attempting to generate raw comment using handler")
            comment = handler.handle(submission.url)
            logging.info("Raw comment generated")
        except Exception as exception:
            logging.error("An error occurred while handling URL = %s",
                          submission.url)
            logging.error("Exception = %s", exception)
            logging.info("Skipping current submission")
            continue

        if comment is None:
            logging.error("comment_raw is None; skipping current submission")
            continue

        logging.info("Generating formatted comment")
        comment_markdown = comment.format_as_md()
        logging.info("Formatted comment generated")

        if len(comment_markdown) < 2 * bot_config.comment_length_limit:
            try:
                logging.info("Attempting to post comment")
                submission.reply(comment_markdown)
                logging.info("Comment posting succeeded")
            except Exception as exception:
                logging.error("Comment is too long to be posted in a single comment")
                logging.error("Exception = %s", exception)
                try:
                    logging.info("Attempting to post two comments")
                    i=1
                    while (comment_markdown[bot_config.comment_length_limit - i] != " "):
                        i += 1
                    part_1 = comment_markdown[0:bot_config.comment_length_limit-i]
                    part_2 = comment_markdown[bot_config.comment_length_limit-i:]

                    if (part_2[0] != ">"):
                        part_2 = ">" + part_2

                    first_comment = submission.reply(part_1)
                    first_comment.reply(part_2)
                    logging.info("Comments posting succeeded")
                except Exception as exception:
                    logging.error("An error occurred while posting two comments")
                    logging.error("Exception = %s", exception)
        else:
            logging.warning("Submission is too long to be posted")