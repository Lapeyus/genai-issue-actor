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
  message STRING(MAX)
)
OPTIONS (
  description = 'Commits in the GitHub public repository.',
  labels = ['public', 'github']
)
""")
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

class TestFormattingTable(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "name": ["Alice", "Bob", "Carol"],
            "age": [20, 25, 30],
        })
        self.expected = "name:Alice,age:20,name:Bob,age:25,name:Carol,age:30"
    
    def test_format_table(self):
        actual = format_table(self.df)
        self.assertEqual(self.expected, actual)

def format_table(df):
    formatted_strings = []
    for row in df.iterrows():
        for col_name in df.columns:
            formatted_strings.append(f"{col_name}:{row[col_name]}")
    return ', '.join(formatted_strings)

if __name__ == "__main__":
    unittest.main()

# Adjust the code to change the webpage icon to a car
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Create a new instance of the Chrome driver
options = Options()
options.add_argument("--window-size=1920,1080")

# Specify the path to the car icon
options.add_argument("--app-icon=path/to/car_icon.ico")

# Create a new Chrome driver with the specified options
driver = webdriver.Chrome(options=options)

# Load the webpage
driver.get("https://www.example.com")