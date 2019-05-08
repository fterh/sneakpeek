import unittest
from unittest import mock, TestCase

import config

# Set ENV to "test" before loading scan module
config.ENV = "test"

from scan import scan
import test_qualify

RAW_COMMENT = "some_raw_comment_text"
FORMATTED_COMMENT = "some_formatted_comment_text"

# Set up mock objects
mock_subreddit = mock.Mock()
mock_subreddit.stream.submissions.return_value = [test_qualify.mock_submission]

mock_handler = mock.Mock()
mock_handler.handle.return_value = RAW_COMMENT


class TestScan(TestCase):
    def setUp(self):
        test_qualify.mock_submission.reset_mock()

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("scan.format_comment")
    def test_success(self,
                     mock_format_comment,
                     mock_HandlerManager,
                     mock_qualify
                     ):
        """
        It should post a reply.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = mock_handler
        mock_format_comment.return_value = FORMATTED_COMMENT

        scan(mock_subreddit)

        test_qualify.mock_submission.reply.assert_called_with(FORMATTED_COMMENT)

    @mock.patch("scan.qualify")
    def test_skip_1(self,
                    mock_qualify
                    ):
        """
        It should not post a reply if the article does not qualify but has not been encountered.
        """
        mock_qualify.return_value = False

        scan(mock_subreddit)

        test_qualify.mock_submission.reply.assert_not_called()

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("scan.format_comment")
    def test_skip_2(self,
                    mock_format_comment,
                    mock_HandlerManager,
                    mock_qualify
                    ):
        """
        It should not post a reply if the article qualifies but is too lengthy.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = mock_handler
        mock_format_comment.return_value = FORMATTED_COMMENT
        original_comment_length_limit = config.COMMENT_LENGTH_LIMIT
        config.COMMENT_LENGTH_LIMIT = 1

        scan(mock_subreddit)

        config.COMMENT_LENGTH_LIMIT = original_comment_length_limit

        test_qualify.mock_submission.reply.assert_not_called()


if __name__ == "__main__":
    unittest.main()
