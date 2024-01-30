import os
import unittest
from unittest.mock import patch

from utility import get_env_variable
from utility import parse_issue_body


class TestUtilityFunctions(unittest.TestCase):
    def test_parse_issue_body_success(self):
        issue_body = 'Some text\n```json\n{"key": "value"}\n```'
        expected = {"key": "value"}
        result = parse_issue_body(issue_body)
        self.assertEqual(result, expected)

    def test_parse_issue_body_invalid_json(self):
        issue_body = 'Some text\n```json\n{key: "value"}\n```'  # Invalid JSON
        result = parse_issue_body(issue_body)
        self.assertIsNone(result)

    def test_parse_issue_body_no_json(self):
        issue_body = "Some text without JSON"
        result = parse_issue_body(issue_body)
        self.assertIsNone(result)

    @patch.dict(os.environ, {"TEST_VAR": "test_value"}, clear=True)
    def test_get_env_variable_success(self):
        result = get_env_variable("TEST_VAR")
        self.assertEqual(result, "test_value")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_variable_not_set(self):
        with self.assertRaises(ValueError):
            get_env_variable("MISSING_VAR")


if __name__ == "__main__":
    unittest.main()
