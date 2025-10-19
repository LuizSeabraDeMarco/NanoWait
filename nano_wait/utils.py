from datetime import datetime

def get_speed_value(speed):
    """Converts speed preset or numeric input to float."""
    speed_map = {"slow": 0.8, "normal": 1.5, "fast": 3.0, "ultra": 6.0}
    if isinstance(speed, str):
        return speed_map.get(speed.lower(), 1.5)
    return float(speed)

def log_message(text: str):
    """Saves messages to nano_wait.log."""
    with open("nano_wait.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
