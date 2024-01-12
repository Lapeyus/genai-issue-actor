```python
import unittest
from main import parse_bigquery_schema
import pandas as pd

class MockDocument:
    def __init__(self, page_content):
        self.page_content = page_content

class TestBigQuerySchemaParsing(unittest.TestCase):
    def setUp(self):
        self.data = [
            MockDocument("""
ddl: CREATE TABLE `bigquery-public-data.github_repos.commits` (
  commit SHA256 NOT NULL,
  author DATE NOT NULL,
  committer DATE NOT NULL,
  message STRING