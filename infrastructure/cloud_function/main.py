import functions_framework
import logging
import json
import os
import base64

from autocoder import Autocoder
from utility import parse_issue_body

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

    if 'action' not in request_json:
        return (json.dumps({"err": 'Request body does not include an "action"'}), 400, return_headers)
    
    if request_json['issue']['assignee'] is not None:
        logger.info(f"Issue already assigned to: {request_json['issue']['assignee']}")
        return (json.dumps({"err": 'Issue already assigned'}), 200, return_headers)

    if request_json['action'] != "opened":
        logger.info(f"ignoring non-new issue notification, action: {request_json['action']}")
        return (json.dumps({"msg": "Ignoring non-new issue notification"}), 200, return_headers)

    git_repo = request_json['repository']['ssh_url']
    git_repo_id = int(request_json['repository']['id'])
    issue_number = int(request_json['issue']['number'])
    issue_body = request_json['issue']['body']

    parsed_body = parse_issue_body(issue_body)    
    logger.info(f"Git repo: {git_repo}")
    logger.info(f"Issue body: {issue_body}")

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
        contributing = None
        try:
            contributing = autocoder_app._fetch_repo_file_contents("CONTRIBUTING.md")
        except:
            logger.info("No existing CONTRIBUTING.md to use.")
            pass

        desired_change = parsed_body["change_request"]["description"]
        autocoder_app.create_branch(contributing=contributing, desired_change=desired_change)
        
        # Iterate through each affected file and create a commit
        for file in parsed_body["change_request"]["affected_files"]:
            existing_code, updated_code = autocoder_app.apply_code_changes(file, desired_change)
            autocoder_app.create_commit(
                existing_code=existing_code, replacement_code=updated_code, contributing=contributing
                # , commit_message=desired_change
            )
        
        autocoder_app.push_remote()
        autocoder_app.create_pr(
            repo_id=git_repo_id,
            issue_number=issue_number,
            commit_message=desired_change
        )
    except BaseException as e:
        return (json.dumps({"err": str(e) }), 500, return_headers)
    finally:
        Autocoder.cleanup_local_dir()

    return (json.dumps({"msg": "ok"}), 200, return_headers)
