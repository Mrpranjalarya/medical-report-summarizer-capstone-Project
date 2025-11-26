# memory/session_service.py
import json
import os
from datetime import datetime

SESSIONS_DIR = ".sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

class SessionService:
    def __init__(self):
        pass

    def save_report(self, payload: dict):
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        path = os.path.join(SESSIONS_DIR, f"report_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return path
