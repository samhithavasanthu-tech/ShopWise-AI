import json
from datetime import datetime


def log_action(action, details):

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "details": details
    }

    try:
        with open("audit_log.json", "r") as file:
            logs = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open("audit_log.json", "w") as file:
        json.dump(logs, file, indent=4)