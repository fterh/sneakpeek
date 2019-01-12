import sqlite3
import unittest
from unittest import mock, TestCase

import config

# Set ENV to "test" before loading scan module
config.ENV = "test"

from database import DatabaseActionEnum
from scan import scan
import test_qualify

# Constants
DB_NAME = config.DATABASE["NAME"]
print(DB_NAME)
DB_SUBMISSIONS_TABLE = config.DATABASE["TABLES"]["SUBMISSIONS"]["NAME"]
DB_SUBMISSIONS_ID = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_NAME"]
DB_SUBMISSIONS_ACTION = config.DATABASE["TABLES"]["SUBMISSIONS"]["ACTION_NAME"]
DB_SUBMISSIONS_INDEX = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_INDEX_NAME"]

RAW_COMMENT = "some_raw_comment_text"
FORMATTED_COMMENT = "some_formatted_comment_text"

# Set up mock objects
mock_subreddit = mock.Mock()
mock_subreddit.new.return_value = [test_qualify.mock_submission]

mock_handler = mock.Mock()
mock_handler.handle.return_value = RAW_COMMENT


class TestScan(TestCase):
    def setUp(self):
        test_qualify.mock_submission.reset_mock()

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("scan.format_comment")
    @mock.patch("scan.DatabaseManager")
    def test_success(self,
                     mock_DatabaseManager,
                     mock_format_comment,
                     mock_HandlerManager,
                     mock_qualify
                     ):
        """
        It should post a reply and record success to the database.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = mock_handler
        mock_format_comment.return_value = FORMATTED_COMMENT

        scan(mock_subreddit)

        test_qualify.mock_submission.reply.assert_called_with(FORMATTED_COMMENT)
        mock_DatabaseManager.write_id.assert_called_with(test_qualify.MOCK_SUBMISSION_ID,
                                                         DatabaseActionEnum.SUCCESS
                                                         )

    @mock.patch("scan.qualify")
    @mock.patch("scan.DatabaseManager")
    def test_skip_1(self,
                    mock_DatabaseManager,
                    mock_qualify
                    ):
        """
        It should not post a reply but record skip to the database
        if the article does not qualify but has not been encountered.
        """
        mock_qualify.return_value = False
        mock_DatabaseManager.check_id.return_value = False

        scan(mock_subreddit)

        test_qualify.mock_submission.reply.assert_not_called()
        mock_DatabaseManager.write_id.assert_called_with(test_qualify.MOCK_SUBMISSION_ID,
                                                         DatabaseActionEnum.SKIP
                                                         )

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("scan.format_comment")
    @mock.patch("scan.DatabaseManager")
    def test_skip_2(self,
                    mock_DatabaseManager,
                    mock_format_comment,
                    mock_HandlerManager,
                    mock_qualify
                    ):
        """
        It should not post a reply but record skip to the database
        if the article qualifies but is too lengthy.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = mock_handler
        mock_format_comment.return_value = FORMATTED_COMMENT
        original_comment_length_limit = config.COMMENT_LENGTH_LIMIT
        config.COMMENT_LENGTH_LIMIT = 1

        scan(mock_subreddit)

        config.COMMENT_LENGTH_LIMIT = original_comment_length_limit

        test_qualify.mock_submission.reply.assert_not_called()
        mock_DatabaseManager.write_id.assert_called_with(test_qualify.MOCK_SUBMISSION_ID,
                                                         DatabaseActionEnum.SKIP
                                                         )

    @mock.patch("scan.qualify")
    @mock.patch("scan.HandlerManager")
    @mock.patch("scan.format_comment")
    @mock.patch("scan.DatabaseManager")
    def test_error(self,
                     mock_DatabaseManager,
                     mock_format_comment,
                     mock_HandlerManager,
                     mock_qualify
                     ):
        """
        It should handle gracefully a ValueError exception raised by the database module
        when writing a submission ID that already exists in the database.
        """
        mock_qualify.return_value = True
        mock_HandlerManager.get_handler.return_value = mock_handler
        mock_format_comment.return_value = FORMATTED_COMMENT
        mock_DatabaseManager.write_id.side_effect = ValueError()

        scan(mock_subreddit)

        test_qualify.mock_submission.reply.assert_called_with(FORMATTED_COMMENT)
        mock_DatabaseManager.write_id.assert_called_with(test_qualify.MOCK_SUBMISSION_ID,
                                                         DatabaseActionEnum.SUCCESS
                                                         )


if __name__ == "__main__":
    unittest.main()
