from jira_utils import add_comment_to_jira
import os
from datetime import datetime


def pytest_runtest_makereport(item, call):
    if call.when != "call":
        return

    build_number = os.getenv("BUILD_NUMBER", "local-run")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if call.excinfo is None:
        message = f"PASS: {item.name}\nBuild: #{build_number}\nTime: {current_time}"
    else:
        message = f"FAIL: {item.name}\nBuild: #{build_number}\nTime: {current_time}"

    try:
        add_comment_to_jira(message)
    except Exception as exc:
        print(f"Jira update skipped for {item.name}: {exc}")
