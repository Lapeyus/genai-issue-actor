```python
import unittest
from main import parse_bigquery_schema

class TestBigQuerySchemaParsing(unittest.TestCase):
    def setUp(self):
        self.data = [
            """
ddl: CREATE TABLE `bigquery-public-data.github_repos.commits` (
  commit SHA256 NOT NULL,
  author DATE NOT NULL,
  committer DATE NOT NULL,
  message STRING(MAX)
)
OPTIONS (
  description = 'Commits in the GitHub public repository.',
  labels = ['public', 'github']
)
"""
        ]
        self.expected = """
Table Name: `bigquery-public-data.github_repos.commits`
   - commit SHA256
   - NOT NULL
   - author DATE
   - NOT NULL
   - committer DATE
   - NOT NULL
   - message STRING
"""

    def test_parse_bigquery_schema(self):
        actual = parse_bigquery_schema(self.data)
        self.assertEqual(self.expected.strip(), actual.strip())

if __name__ == "__main__":
    unittest.main()
```