---
name: Code Modification Request
about: Request a code change or upgrade
title: "[MODIFY]: "
labels: ["genai", "bot"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        hi!
  - type: input
    id: files_to_scan
    attributes:
      label: Files to Scan
      description: List the files that need to be scanned, separated by commas.
      placeholder: "file1.py, file2.py"
    validations:
      required: true
  - type: textarea
    id: proposed_changes
    attributes:
      label: Proposed Changes
      description: Describe the changes or upgrades proposed for each file, and specify the location of any associated unit tests.
      placeholder: "file1.py: Description of change, Unit test: tests/test_file1.py"
      render: json
    validations:
      required: true