class TestBigQuerySchemaParsing(unittest.TestCase):
    def setUp(self):
        self.data = [
            MockDocument("""
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
""")
        ]
        self.expected = """
Table Name: