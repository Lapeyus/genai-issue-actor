import base64
import json
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from main import event_processor


class TestEventProcessor(unittest.TestCase):
    @patch("your_module_name.Autocoder")  # Mock the Autocoder class
    @patch.dict(
        "os.environ",
        {
            "PRIVATE_KEY": base64.b64encode(b"mock_private_key").decode("utf-8"),
            "PUBLIC_KEY": base64.b64encode(b"mock_public_key").decode("utf-8"),
            "PASS_KEY": base64.b64encode(b"mock_pass_key").decode("utf-8"),
            "GEMINI_API_KEY": "mock_gemini_api_key",
            "GITHUB_PAT": "mock_github_pat",
            "GENAI_MODEL": "mock_genai_model",
        },
    )
    def test_event_processor(self, mock_autocoder):
        cloud_event_data = {
            "message": {
                "data": base64.b64encode(
                    json.dumps(
                        {
                            "repository": {
                                "ssh_url": "git@github.com:example/repo.git",
                                "id": "123456",
                            },
                            "issue": {
                                "number": "42",
                                "body": {
                                    "change_request": {
                                        "description": "Update README",
                                        "affected_files": ["README.md"],
                                    }
                                },
                            },
                        }
                    ).encode("utf-8")
                ).decode("utf-8")
            }
        }
        mock_cloud_event = MagicMock()
        mock_cloud_event.data = cloud_event_data

        # Mock Autocoder methods
        mock_autocoder_instance = mock_autocoder.return_value
        mock_autocoder_instance.clone_repository.return_value = None
        mock_autocoder_instance.create_branch.return_value = None
        mock_autocoder_instance.apply_code_changes.return_value = (
            "old_code",
            "new_code",
        )
        mock_autocoder_instance.create_commit.return_value = None
        mock_autocoder_instance.push_remote.return_value = None
        mock_autocoder_instance.create_pr.return_value = None

        # Test event_processor
        event_processor(mock_cloud_event)

        # Verify that Autocoder methods are called as expected
        mock_autocoder_instance.clone_repository.assert_called_with(
            "git@github.com:example/repo.git"
        )
        mock_autocoder_instance.create_branch.assert_called_with(
            desired_change="Update README"
        )
        mock_autocoder_instance.apply_code_changes.assert_called_with(
            "README.md", "Update README"
        )
        mock_autocoder_instance.create_commit.assert_called_with(
            existing_code="old_code", replacement_code="new_code"
        )
        mock_autocoder_instance.push_remote.assert_called()
        mock_autocoder_instance.create_pr.assert_called_with(
            repo_id=123456, issue_number=42
        )


if __name__ == "__main__":
    unittest.main()
