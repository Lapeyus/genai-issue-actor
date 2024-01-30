import json
import os


def parse_issue_body(issue_body):
    # Extract JSON part from the issue body
    # Assuming the JSON part is enclosed in triple backticks (```)
    start = issue_body.find("```json") + 7  # 7 to skip over the ```json
    end = issue_body.find("```", start)
    json_str = issue_body[start:end].strip()

    # Parse the JSON string
    try:
        parsed_json = json.loads(json_str)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value
