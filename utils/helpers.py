from pathlib import Path
import json
import time


PROJECT_ROOT = Path(__file__).resolve().parents[1]
USERS_PATH = PROJECT_ROOT / "data" / "users.json"


def generate_random_email() -> str:
    timestamp = time.time_ns()
    return f"test{timestamp}@example.com"


def load_users() -> dict:
    with USERS_PATH.open(encoding="utf-8") as f:
        return json.load(f)
