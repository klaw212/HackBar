from datetime import datetime
import os

LOG_FILE = "hackbar.log"


def log(event: str, data: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {event}: {data}\n"

    with open(LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
        f.write(line)
