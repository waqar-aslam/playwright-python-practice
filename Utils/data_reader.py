import json
import os
from pathlib import Path

# Real credentials are not committed. Locally, copy data/credentials.example.json to
# data/credentials.json; in CI, point TEST_CREDENTIALS_FILE at a secret file.
DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "credentials.json"
data_file = Path(os.environ.get("TEST_CREDENTIALS_FILE", DEFAULT_DATA_FILE))

if not data_file.is_file():
    raise FileNotFoundError(
        f"Credentials file not found: {data_file}. Copy data/credentials.example.json "
        "to data/credentials.json or set TEST_CREDENTIALS_FILE."
    )

with open(data_file, "r") as f:
    data = json.load(f)


def get_users():
    return data["user_credentials"]
