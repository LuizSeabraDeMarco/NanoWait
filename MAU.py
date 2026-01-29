import os
import json
import uuid
from datetime import datetime

USAGE_FILE = os.path.expanduser("~/.nano_wait_usage.jsonl")
ID_FILE = os.path.expanduser("~/.nano_wait_uid")


def telemetry_enabled() -> bool:
    """
    Telemetry is ON by default.
    Disable with: export NANO_WAIT_TELEMETRY=0
    """
    return os.getenv("NANO_WAIT_TELEMETRY", "1") != "0"


def get_anon_id() -> str:
    """
    Persistent, anonymous, local-only user identifier.
    """
    if os.path.exists(ID_FILE):
        try:
            return open(ID_FILE).read().strip()
        except Exception:
            pass

    uid = str(uuid.uuid4())

    try:
        with open(ID_FILE, "w") as f:
            f.write(uid)
    except Exception:
        pass

    return uid


def log_usage_event(event: str, version: str):
    """
    Log a minimal anonymous usage event.
    One event per execution/session.
    """
    if not telemetry_enabled():
        return

    data = {
        "anon_id": get_anon_id(),
        "event": event,
        "version": version,
        "ts": datetime.utcnow().isoformat()
    }

    try:
        with open(USAGE_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception:
        # telemetry must NEVER break user code
        pass
