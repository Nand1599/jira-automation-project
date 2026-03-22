import json
import os
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

ISSUE_KEY = "KAN-1"


def load_local_env(env_path=".env"):
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


load_local_env()


def add_comment_to_jira(
    comment_text="Test failed! This comment was added using Python automation.",
    issue_key=ISSUE_KEY,
    jira_url=None,
    email=None,
    api_token=None,
):
    jira_url = jira_url or os.getenv("JIRA_URL")
    email = email or os.getenv("JIRA_EMAIL")
    api_token = api_token or os.getenv("JIRA_API_TOKEN")

    if not jira_url or not email or not api_token:
        raise ValueError(
            "Missing Jira configuration. Set JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN."
        )

    url = f"{jira_url}/rest/api/3/issue/{issue_key}/comment"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text,
                        }
                    ],
                }
            ],
        }
    }

    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
    return response


if __name__ == "__main__":
    response = add_comment_to_jira()
    print(response.status_code)
    print(response.text)
