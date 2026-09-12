import json
from datetime import datetime, timezone
from pathlib import Path
from app.core.config import SUBMISSIONS_FILE

def save_submission(record: dict):
    SUBMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SUBMISSIONS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def utc_now():
    return datetime.now(timezone.utc).isoformat()
