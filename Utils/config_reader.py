import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def available_envs():
    return sorted(p.stem for p in CONFIG_DIR.glob("*.json"))


def load_config(env):
    """Return the settings for one environment, read from config/<env>.json."""
    config_file = CONFIG_DIR / f"{env}.json"
    if not config_file.is_file():
        raise FileNotFoundError(f"No config for environment {env!r}. Available: {available_envs()}")
    with open(config_file) as f:
        return json.load(f)
