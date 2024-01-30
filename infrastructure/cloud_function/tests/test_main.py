import json
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from main import handle_issue


class TestHandleIssue(unittest.TestCase):
    @patch.dict(
        "os.environ",
        {"PROJECT_ID": "test_project_id", "PUBSUB_TOPIC": "test_topic_name"},
    )
    def setUp(self):
        self.request = MagicMock()
        self.request.get_json = MagicMock()

    @patch("main.publisher")
    def test_no_action(self, mock_publisher):
        self.request.get_json.return_value = {"issue": {"assignee": None}}
        response = handle_issue(self.request)
        self.assertEqual(
            response[0],
            json.dumps({"err": 'Request body does not include an "action"'}),
        )
        self.assertEqual(response[1], 400)

    @patch("main.publisher")
    def test_issue_already_assigned(self, mock_publisher):
        self.request.get_json.return_value = {
            "action": "opened",
            "issue": {"assignee": "someone@example.com"},
        }
        response = handle_issue(self.request)
        self.assertEqual(response[0], json.dumps({"err": "Issue already assigned"}))
        self.assertEqual(response[1], 200)

    @patch("main.publisher")
    def test_non_new_issue(self, mock_publisher):
        self.request.get_json.return_value = {
            "action": "edited",
            "issue": {"assignee": None},
        }
        response = handle_issue(self.request)
        self.assertEqual(
            response[0], json.dumps({"msg": "Ignoring non-new issue notification"})
        )
        self.assertEqual(response[1], 200)

    @patch("main.publisher")
    def test_success(self, mock_publisher):
        self.request.get_json.return_value = {
            "action": "opened",
            "issue": {"body": "This is a test issue.", "assignee": None},
        }
        response = handle_issue(self.request)
        self.assertEqual(response[0], json.dumps({"msg": "ok"}))
        self.assertEqual(response[1], 200)


if __name__ == "__main__":
    unittest.main()
