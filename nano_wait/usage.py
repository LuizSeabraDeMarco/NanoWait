# nano_wait/usage.py
from datetime import datetime

def log_usage_event(event: str, metadata: dict | None = None):
    timestamp = datetime.utcnow().isoformat()
    print(f"[NanoWait][USAGE] {timestamp} | {event} | {metadata}")
