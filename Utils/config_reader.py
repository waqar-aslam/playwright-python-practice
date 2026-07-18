import json
from pathlib import Path

config_file = Path(__file__).resolve().parent.parent / "config" / "settings.json"
print(config_file)
with open(config_file) as f:
    settings = json.load(f)

def get_settings():
    return settings

def get_url(name):
    """Return a URL by its name."""
    return settings["urls"][name]