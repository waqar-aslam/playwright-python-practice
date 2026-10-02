import json
from pathlib import Path

def test_read_filepath():
    file = Path(__file__).resolve().parents[2] / "data" / "credentials.json"
    print(file)
    with open(file, "r") as f:
        data = json.load(f)
        # Don't print the data itself - it contains passwords
        print(f"Loaded {len(data['user_credentials'])} users")

def test_read_settings():
    file = Path(__file__).resolve().parents[2] / "config" / "settings.json"
    print(file)
    with open(file, "r") as f:
        data = json.load(f)
        print(data)