import base64
import json
import logging

import functions_framework
from autocoder import Autocoder
from cloudevents.http import CloudEvent
from utility import get_env_variable

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

github_private_key = base64.b64decode(get_env_variable("PRIVATE_KEY")).decode("utf-8")
github_public_key = base64.b64decode(get_env_variable("PUBLIC_KEY")).decode("utf-8")
git_key_passphrase = base64.b64decode(get_env_variable("PASS_KEY")).decode("utf-8")
gemini_api_key = get_env_variable("GEMINI_API_KEY")
github_pat = get_env_variable("GITHUB_PAT")
llm = get_env_variable("GENAI_MODEL")


@functions_framework.cloud_event
def event_processor(cloud_event: CloudEvent) -> None:
    message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    request_json = json.loads(message_data)
    logger.info(request_json)

    git_repo = request_json["repository"]["ssh_url"]
    git_repo_id = int(request_json["repository"]["id"])
    issue_number = int(request_json["issue"]["number"])
    issue_body = request_json["issue"]["body"]
    desired_change = issue_body["change_request"]["description"]
    affected_files = issue_body["change_request"]["affected_files"]

    autocoder_app = Autocoder(
        github_private_key,
        github_public_key,
        github_pat,
        git_key_passphrase,
        llm=llm,
        gemini_api_key=gemini_api_key,
    )

    try:
        autocoder_app.clone_repository(git_repo)
        autocoder_app.create_branch(desired_change=desired_change)

        for file in affected_files:
            existing_code, updated_code = autocoder_app.apply_code_changes(
                file, desired_change
            )
            autocoder_app.create_commit(
                existing_code=existing_code, replacement_code=updated_code
            )

        autocoder_app.push_remote()
        autocoder_app.create_pr(repo_id=git_repo_id, issue_number=issue_number)
        logger.info("Issue processed successfully")
    except BaseException as e:
        logger.error(f"Error processing issue: {e}")
    finally:
        Autocoder.cleanup_local_dir()
