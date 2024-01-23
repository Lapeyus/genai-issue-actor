import functions_framework
import logging
import json
import os
import base64

from autocoder import Autocoder
from utility import parse_issue_body

# Setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Environment variables
project_id = os.getenv('PROJECT_ID')
location = os.getenv('LOCATION')
github_pat = os.getenv('GITHUB_PAT')
github_private_key = base64.b64decode(os.getenv("PRIVATE_KEY")).decode('utf-8')
github_public_key = base64.b64decode(os.getenv("PUBLIC_KEY")).decode('utf-8')
git_key_passphrase = base64.b64decode(os.getenv("PASS_KEY")).decode('utf-8')
llm = os.getenv('GENAI_MODEL')
gemini_api_key = os.getenv("GEMINI_API_KEY")

@functions_framework.http
def handle_issue(request):
    request_json = request.get_json(silent=True)
    return_headers = {"Content-Type": "application/json"}

    # Validate request
    if 'action' not in request_json or 'issue' not in request_json:
        return (json.dumps({"err": 'Invalid request format'}), 400, return_headers)

    # Check for issue assignment
    if request_json['issue']['assignee'] is not None:
        logger.info(f"Issue already assigned to: {request_json['issue']['assignee']}")
        return (json.dumps({"err": 'Issue already assigned'}), 200, return_headers)

    # Filter out non-opened issues
    if request_json['action'] != "opened":
        logger.info(f"Ignoring non-new issue notification, action: {request_json['action']}")
        return (json.dumps({"msg": "Ignoring non-new issue notification"}), 200, return_headers)

    # Extracting repository and issue details
    git_repo = request_json['repository']['ssh_url']
    git_repo_id = int(request_json['repository']['id'])
    issue_number = int(request_json['issue']['number'])
    issue_body = request_json['issue']['body']
    parsed_body = parse_issue_body(issue_body)

    logger.info(f"Git repo: {git_repo}")
    logger.info(f"Issue body: {issue_body}")

    # Initialize Autocoder
    autocoder_app = Autocoder(
        github_private_key,
        github_public_key,
        github_pat,
        git_key_passphrase,
        llm=llm,
        gemini_api_key=gemini_api_key
    )

    try:
        autocoder_app.clone_repository(git_repo)
        contributing = autocoder_app.fetch_repo_file_contents("CONTRIBUTING.md", optional=True)

        # Initialize commit messages list
        commit_messages = []

        # Create branch and apply changes
        autocoder_app.create_branch(contributing=contributing, desired_change=parsed_body["change_request"]["description"])
        for file_path, file_change in parsed_body["change_request"]["affected_files"].items(): 
            existing_code, updated_code = autocoder_app.apply_code_changes(file_path, file_change)
            # autocoder_app.update_unit_tests("tests/test_main.py", updated_code)
            commit_message = autocoder_app.create_commit(existing_code, updated_code, contributing)
            commit_messages.append(commit_message)

        # Push changes and create PR
        autocoder_app.push_remote()
        if commit_messages:
            autocoder_app.create_pr(git_repo_id, issue_number, parsed_body["change_request"]["description"])
        else:
            raise ValueError("No commit messages were created. Unable to create a pull request.")
    except BaseException as e:
        return (json.dumps({"err": str(e)}), 500, return_headers)
    finally:
        Autocoder.cleanup_local_dir()

    return (json.dumps({"msg": "ok"}), 200, return_headers)
