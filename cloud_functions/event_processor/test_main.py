import unittest
from unittest.mock import patch, MagicMock
import base64
import json
from main import event_processor

class TestEventProcessor(unittest.TestCase):
    @patch("main.Autocoder")  # Adjust this import path to where Autocoder is defined
    @patch.dict("os.environ", {
        "PRIVATE_KEY": "c3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCQVFDN056N3FiQzU4ZUorZFRjZGNIUTNURXQybzdSTFFiU3VvMWNLK2EvUnhGVklQQVI5VlB1UXJ3UFlmS1RwUGR2aVBHTFVIVXl2YXh0dGRpcXkveXcrVEFvOVRYYit6TEZBbjZoeGN5TXhQa2ZhYjhqYUZ2dGR4U2xzZDhieU5nMFAzbytONVVZaVdKMUZPRTFiMzREVjVJamFEekg2ZGlnclJHNUZKM1RLRkxvL2c4dVF3OFpCbHViOVcvNzRzcEFBd2I3QmRWdnQvcXcrcUxBaXJ2ODA4elY1SjlzcHpObkdaRU1pUlUxaTl6c1dNcURWQ2RzR0t5VnNyT1NpZVE2V0lXRkVIMWR2QWZpS2pIWWIwVDg3QVJvQWJ0RTN4N05NQnB5alRiVmgvWEc2MUwvZVdrZWQzYUZ5ckRxYTlxVStDdDNMVko1Mmx4VkhhcHhLSXEzT3IganZpbGxhcnJlYWwK",
        "PUBLIC_KEY": "c3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCQVFDN056N3FiQzU4ZUorZFRjZGNIUTNURXQybzdSTFFiU3VvMWNLK2EvUnhGVklQQVI5VlB1UXJ3UFlmS1RwUGR2aVBHTFVIVXl2YXh0dGRpcXkveXcrVEFvOVRYYit6TEZBbjZoeGN5TXhQa2ZhYjhqYUZ2dGR4U2xzZDhieU5nMFAzbytONVVZaVdKMUZPRTFiMzREVjVJamFEekg2ZGlnclJHNUZKM1RLRkxvL2c4dVF3OFpCbHViOVcvNzRzcEFBd2I3QmRWdnQvcXcrcUxBaXJ2ODA4elY1SjlzcHpObkdaRU1pUlUxaTl6c1dNcURWQ2RzR0t5VnNyT1NpZVE2V0lXRkVIMWR2QWZpS2pIWWIwVDg3QVJvQWJ0RTN4N05NQnB5alRiVmgvWEc2MUwvZVdrZWQzYUZ5ckRxYTlxVStDdDNMVko1Mmx4VkhhcHhLSXEzT3IganZpbGxhcnJlYWwK",
        "PASS_KEY": "c3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCQVFDN056N3FiQzU4ZUorZFRjZGNIUTNURXQybzdSTFFiU3VvMWNLK2EvUnhGVklQQVI5VlB1UXJ3UFlmS1RwUGR2aVBHTFVIVXl2YXh0dGRpcXkveXcrVEFvOVRYYit6TEZBbjZoeGN5TXhQa2ZhYjhqYUZ2dGR4U2xzZDhieU5nMFAzbytONVVZaVdKMUZPRTFiMzREVjVJamFEekg2ZGlnclJHNUZKM1RLRkxvL2c4dVF3OFpCbHViOVcvNzRzcEFBd2I3QmRWdnQvcXcrcUxBaXJ2ODA4elY1SjlzcHpObkdaRU1pUlUxaTl6c1dNcURWQ2RzR0t5VnNyT1NpZVE2V0lXRkVIMWR2QWZpS2pIWWIwVDg3QVJvQWJ0RTN4N05NQnB5alRiVmgvWEc2MUwvZVdrZWQzYUZ5ckRxYTlxVStDdDNMVko1Mmx4VkhhcHhLSXEzT3IganZpbGxhcnJlYWwK",
        "GEMINI_API_KEY": "mock_gemini_api_key",
        "GITHUB_PAT": "mock_github_pat", 
        "GENAI_MODEL": "gemini", 
    }, clear=True)
    def test_event_processor_success(self, mock_autocoder):
        # Setup test data and mocks
        cloud_event_data = {
            "message": {
                "data": base64.b64encode(json.dumps({
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
                }).encode("utf-8")).decode("utf-8")
            }
        }
        mock_cloud_event = MagicMock(data=cloud_event_data)

        # Setup expected calls and return values on the mock_autocoder instance
        autocoder_instance = mock_autocoder.return_value
        autocoder_instance.clone_repository.return_value = None
        autocoder_instance.create_branch.return_value = None
        autocoder_instance.apply_code_changes.return_value = ("old_code", "new_code")
        autocoder_instance.create_commit.return_value = None
        autocoder_instance.push_remote.return_value = None
        autocoder_instance.create_pr.return_value = None

        # Execute the function under test
        event_processor(mock_cloud_event)

        # Assertions to verify the expected behavior
        autocoder_instance.clone_repository.assert_called_once_with("git@github.com:example/repo.git")
        autocoder_instance.create_branch.assert_called_once_with(desired_change="Update README")
        autocoder_instance.apply_code_changes.assert_called_once_with("README.md", "Update README")
        autocoder_instance.create_commit.assert_called_once_with(existing_code="old_code", replacement_code="new_code")
        autocoder_instance.push_remote.assert_called_once()
        autocoder_instance.create_pr.assert_called_once_with(repo_id=123456, issue_number=42)

if __name__ == '__main__':
    unittest.main()
