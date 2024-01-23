import json
import re

def parse_to_json(string_input):
    string_input = re.sub(r'^```json\r\n|\r\n```$', '', string_input, flags=re.MULTILINE)
    string_input = string_input.replace('\\n', '').replace('\\r', '').replace('\\"', '"')

    try:
        json_data = json.loads(string_input)
        return json_data
    except json.JSONDecodeError as e:
        json_data = {"error": f"JSON decoding error: {e}"}


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

def extract_values_from_json(parsed_json):
    if parsed_json and "change_request" in parsed_json:
        change_request = parsed_json["change_request"]
        
        branch_name = change_request.get("branch_name")
        description = change_request.get("description")
        
        affected_files = change_request.get("affected_files", [])
        
        # Assuming there might be multiple files in affected_files
        for file_info in affected_files:
            file_name = file_info.get("file")
            file_change = file_info.get("change")
            unit_test_path = file_info.get("unit_test_path")

            # Process each file's information here
            # For example, you can print them or use them further in your code
            print(f"File: {file_name}, Change: {file_change}, Unit Test Path: {unit_test_path}")
        
        return branch_name, description, affected_files

    else:
        print("Invalid or empty JSON.")
        return None, None, None

