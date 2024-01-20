---
name: Genai Request a code change or upgrade
about: Genai Request a code change or upgrade
title: "[GENAI]-"
labels: enhancement,genai
assignees: ''

---
```json
{
  "change_request": {
    "branch_name": "branch_name",
    "description": "Description of the change",
    "affected_files": [
      {
        "file": "main.py",
        "change": "Description of the changes for main.py",
        "unit_test_path": "tests/main.py"
      },
      // {
      //   "file": "file2.py",
      //   "change": "Description of the change for file2.py",
      //   "unit_test_path": "tests/test_file2.py"
      // }
    ]
  }
}
```
