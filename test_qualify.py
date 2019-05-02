import unittest
from unittest import mock, TestCase

from qualify import qualify

# Set up a mock submission object
MOCK_SUBMISSION_ID = "foo123"
MOCK_SUBMISSION_URL = "bar123"

mock_submission = mock.Mock()
mock_submission.id = MOCK_SUBMISSION_ID
mock_submission.url = MOCK_SUBMISSION_URL


class TestQualify(TestCase):

    @mock.patch("qualify.HandlerManager")
    def test_qualify_should_return_true(self, mock_HandlerManager):
        # (1) Submission is a link,
        # (2) Submission has not been previously encountered
        # (3) Submission has a Handler

        mock_submission.is_self = False
        mock_HandlerManager.has_handler.return_value = True

        self.assertTrue(qualify(mock_submission))

        # Also assert that qualify() did call the method HandlerManager.has_handler()
        mock_HandlerManager.has_handler.assert_called_with(MOCK_SUBMISSION_URL)

    @mock.patch("qualify.HandlerManager")
    def test_qualify_should_return_false_1(self, mock_HandlerManager):
        # Submission is not a link

        mock_submission.is_self = True
        mock_HandlerManager.has_handler.return_value = True

        self.assertFalse(qualify(mock_submission))

        # Also assert that qualify() did call the method HandlerManager.has_handler()
        mock_HandlerManager.has_handler.assert_called_with(MOCK_SUBMISSION_URL)

    @mock.patch("qualify.HandlerManager")
    def test_qualify_should_return_false_3(self, mock_HandlerManager):
        # Submission does not have a Handler

        mock_submission.is_self = False
        mock_HandlerManager.has_handler.return_value = False

        self.assertFalse(qualify(mock_submission))

        # Also assert that qualify() did call the method HandlerManager.has_handler()
        mock_HandlerManager.has_handler.assert_called_with(MOCK_SUBMISSION_URL)


if __name__ == "__main__":
    unittest.main()
