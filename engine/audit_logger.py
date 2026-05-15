"""
Audit Logger
Json for future integration (ELK, SIEM, ecc.)
"""

import os
import json
from datetime import datetime, timezone


LOG_FILE = "logs/audit.log"


def _ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


def log_event(event_type, decision, result, reason=None):
    """
    event_type: decision | execution | error
    decision: dict originale
    result: allowed / executed / skipped / failed
    reason: opzionale
    """

    _ensure_log_dir()

    entry = {
        "timestamp": _timestamp(),
        "event_type": event_type,
        "action": decision.get("action"),
        "target": decision.get("target"),
        "result": result,
        "reason": reason,
        "signal": decision.get("signal"),
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        print(f"[AUDIT ERROR] {e}")
