import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "execution_logs.json")

os.makedirs(LOG_DIR, exist_ok=True)


def log_execution(step, state, status="success", details=""):

    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "repository": state.get("repository"),
        "question": state.get("question"),
        "step": step,
        "status": status,
        "details": details,
        "sources": state.get("sources", [])
    }

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    else:
        logs = []

    logs.append(log)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)