import json
import logging
import hmac
import hashlib
import functions_framework
from google.cloud import pubsub_v1
from utility import get_env_variable
from utility import parse_issue_body

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

project_id = get_env_variable("PROJECT_ID")
pubsub_topic = get_env_variable("PUBSUB_TOPIC")
github_pat = get_env_variable("GITHUB_PAT")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, pubsub_topic)

@functions_framework.http
def handle_issue(request):    
    return_headers = {"Content-Type": "application/json"}

    # Verify the request
    signature = request.headers.get('X-Hub-Signature-256')
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        print('Error: wrong hash algorithm used')
        return (
            json.dumps({"err": 'Invalid signature'}),
            403,
            return_headers,
        )
    mac = hmac.new(github_pat.encode(), msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        print('Error: signature does not match')
        return (
            json.dumps({"err": 'Invalid signature'}),
            403,
            return_headers,
        )
        
    request_json = request.get_json(silent=True)
    if "action" not in request_json:
        logger.info("Request body does not include an action")
        return (json.dumps({
            "err": 'Request body does not include an "action"'
        }),
                400,
                return_headers,
            )

    if request_json["issue"]["assignee"] is not None:
        logger.info(
f"Issue already assigned to: {request_json['issue']['assignee']}"
        )
        return (json.dumps({
            "err": "Issue already assigned"
        }),
                200,
                return_headers,
            )

    if request_json["action"] != "opened":
        logger.info(
f"ignoring non-new issue notification, action: {request_json['action']}"
        )
        return (json.dumps({
            "msg": "Ignoring non-new issue notification"
        }),
                200,
                return_headers,
            )
    try:
        request_json["issue"]["body"] = parse_issue_body(request_json["issue"]["body"])
        publisher.publish(topic_path, json.dumps(request_json).encode("utf-8"))
        logger.info("Sent to processor queue")
        return (json.dumps({
            "msg": "ok"
        }),
                200,
                return_headers,
            )
    except BaseException as e:
        return (json.dumps({
            "err": str(e)}), 500, return_headers)
