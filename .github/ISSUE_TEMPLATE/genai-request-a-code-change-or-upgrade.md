---
name: Genai Request a code change or upgrade
about: Genai Request a code change or upgrade
title: "[GENAI]"
labels: enhancement
assignees: ''

---

```json
{
  "change_request": {
    "files_to_scan": [
      "file1.py",
      "file2.py"
    ],
    "proposed_changes": [
      {
        "file": "file1.py",
        "change": "Description of the change for file1.py",
        "unit_test_path": "tests/test_file1.py"
      },
      {
        "file": "file2.py",
        "change": "Description of the change for file2.py",
        "unit_test_path": "tests/test_file2.py"
      }
    ]
  }
}
```
