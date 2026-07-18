import json
from pathlib import Path

def test_read_filepath():
    file = Path(__file__).resolve().parent.parent / "data" / "credentials.json"
    print(file)
    with open(file, "r") as f:
        data = json.load(f)
        print(data)

def test_read_settings():
    file = Path(__file__).resolve().parent.parent / "config" / "settings.json"
    print(file)
    with open(file, "r") as f:
        data = json.load(f)
        print(data)