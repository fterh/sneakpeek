"""Test the scan.py module."""


import unittest
from unittest import mock, TestCase

import config
from comment import Comment

# Set ENV to "test" before loading scan module
config.ENV = "test"

from scan import scan
from config import bot_config
import test_qualify

RAW_COMMENT = Comment(title='This is a thing', body='some_raw_comment_text')
FORMATTED_COMMENT = "some_formatted_comment_text"

# Set up mock objects
MOCK_SUBREDDIT = mock.Mock()
MOCK_SUBREDDIT.stream.submissions.return_value = [test_qualify.MOCK_SUBMISSION]

MOCK_HANDLER = mock.Mock()
MOCK_HANDLER.handle.return_value = RAW_COMMENT


class TestScan(TestCase):
    """Test the scan.py module."""

    def setUp(self):
        test_qualify.MOCK_SUBMISSION.reset_mock()

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("comment.Comment.format_as_md")
    def test_success(self,
                     mock_comment_format,
                     mock_HandlerManager,
                     mock_qualify
                     ):
        """
        It should post a reply.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = MOCK_HANDLER
        mock_comment_format.return_value = FORMATTED_COMMENT

        scan(MOCK_SUBREDDIT)

        test_qualify.MOCK_SUBMISSION.reply.assert_called_with(FORMATTED_COMMENT)

    @mock.patch("scan.qualify")
    def test_skip_1(self,
                    mock_qualify
                    ):
        """
        It should not post a reply if the article does not qualify but has not been encountered.
        """
        mock_qualify.return_value = False

        scan(MOCK_SUBREDDIT)

        test_qualify.MOCK_SUBMISSION.reply.assert_not_called()

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("comment.Comment.format_as_md")
    def test_skip_2(self,
                    mock_comment_format,
                    mock_HandlerManager,
                    mock_qualify
                    ):
        """
        It should not post a reply if the article qualifies but is too lengthy.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = MOCK_HANDLER
        mock_comment_format.return_value = FORMATTED_COMMENT
        original_comment_length_limit = bot_config.comment_length_limit

        bot_config.comment_length_limit = 1

        scan(MOCK_SUBREDDIT)

        bot_config.comment_length_limit = original_comment_length_limit

        test_qualify.MOCK_SUBMISSION.reply.assert_not_called()


if __name__ == "__main__":
    unittest.main()
