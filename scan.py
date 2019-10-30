"""Monitor a Subreddit for new submissions."""

import logging
import config
from handler import HandlerManager
from comment import format_comment
from qualify import qualify


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

        comment_raw = None
        try:
            logging.info("Attempting to generate raw comment using handler")
            comment_raw = handler.handle(submission.url)
            logging.info("Raw comment generated")
        except Exception as exception:
            logging.error("An error occurred while handling URL = %s",
                          submission.url)
            logging.error("Exception = %s", exception)
            logging.info("Skipping current submission")
            continue

        if comment_raw is None:
            logging.error("comment_raw is None; skipping current submission")
            continue

        logging.info("Generating formatted comment")
        comment_markdown = format_comment(comment_raw)
        logging.info("Formatted comment generated")

        if len(comment_markdown) < 2*config.COMMENT_LENGTH_LIMIT:
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
                    while (comment_markdown[config.COMMENT_LENGTH_LIMIT-i] != " "):
                        i += 1
                    part_1 = comment_markdown[0: config.COMMENT_LENGTH_LIMIT-i]
                    part_2 = comment_markdown[config.COMMENT_LENGTH_LIMIT-i:]

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