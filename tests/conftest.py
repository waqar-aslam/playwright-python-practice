import os

import pytest
from playwright.sync_api import Playwright

from Utils.APIUtils import APIUtils
from Utils.config_reader import available_envs, load_config

ENV_CONFIG_KEY = pytest.StashKey[dict]()


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=os.environ.get("TEST_ENV", "dev"),
        help=f"Environment config from config/<env>.json (default: $TEST_ENV or dev). Available: {available_envs()}",
    )


def pytest_configure(config):
    env_config = load_config(config.getoption("--env"))
    config.stash[ENV_CONFIG_KEY] = env_config
    # pytest-base-url: an explicit --base-url wins, otherwise use the environment's.
    # pytest-playwright passes base_url to every browser context, so page.goto("/client/") works.
    if not config.getoption("base_url"):
        config.option.base_url = env_config["base_url"]

    # Under pytest-xdist every worker would write to the same log file; give each its own.
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    log_file = config.getoption("log_file") or config.getini("log_file")
    if worker_id and log_file:
        root, ext = os.path.splitext(log_file)
        config.option.log_file = f"{root}_{worker_id}{ext}"


@pytest.fixture(scope="session")
def env_config(pytestconfig):
    return pytestconfig.stash[ENV_CONFIG_KEY]


@pytest.fixture(scope="session")
def api_utils(playwright: Playwright, env_config):
    """Session-wide APIUtils; it caches one token per user."""
    return APIUtils(playwright, env_config["api_base_url"])
