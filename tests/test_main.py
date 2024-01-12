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
                  description = 'Commits in the GitHub public repository.',
                  labels = ['public', 'github']
                )
                """
            }
        ]

        expected = """
        Table Name: `bigquery-public-data.github_repos.commits`

        - commit SHA256 NOT NULL
        - author DATE NOT NULL
        - committer DATE NOT NULL
        - message STRING(MAX)
        """

        actual = parse_bigquery_schema(data)

        self.assertEqual(expected, actual)


class TestFormattingTable(unittest.TestCase):
    def test_format_table(self):
        df = pd.DataFrame(
            {
                "name": ["Alice", "Bob", "Carol"],
                "age": [20, 25, 30],
            }
        )

        expected = "name:Alice,age:20,name:Bob,age:25,name:Carol,age:30"

        actual = format_table(df)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
