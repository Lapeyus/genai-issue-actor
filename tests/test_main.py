import unittest

from main import parse_bigquery_schema, format_table


class TestBigQuerySchemaParsing(unittest.TestCase):
    def test_parse_bigquery_schema(self):
        data = [
            {
                "page_content": """
                ddl: CREATE TABLE `bigquery-public-data.github_repos.commits` (
                  commit SHA256 NOT NULL,
                  author DATE NOT NULL,
                  committer DATE NOT NULL,
                  message STRING(MAX)
                )
                OPTIONS (
                  description = 'Commits in the GitHub