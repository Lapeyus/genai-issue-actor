import json
import os


def parse_issue_body(issue_body):
    start = issue_body.find("```json") + 7
    end = issue_body.find("```", start)
    json_str = issue_body[start:end].strip()

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
