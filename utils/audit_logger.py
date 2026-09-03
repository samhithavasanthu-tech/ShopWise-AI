import json
import os
from datetime import datetime


# -----------------------------------
# PROJECT ROOT
# -----------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

AUDIT_FILE = os.path.join(
    PROJECT_ROOT,
    "audit_log.json"
)


# -----------------------------------
# LOG ACTION
# -----------------------------------

def log_action(action, details):
    """
    Save an AI, blockchain, or review event
    to the ShopWise AI audit trail.
    """

    log_entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "action": action,
        "details": details
    }

    # Load existing logs
    try:

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            logs = json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        logs = []


    # Add new log
    logs.append(
        log_entry
    )


    # Save logs
    with open(
        AUDIT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4,
            ensure_ascii=False
        )