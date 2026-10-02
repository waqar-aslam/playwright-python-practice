# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Playwright + Python (pytest) learning/practice repo. The standalone concept demos (locators, alerts, windows, frames, web tables, fixtures) live under `tests/demos/` and are auto-marked `demo` by `tests/demos/conftest.py`. The framework pieces are the API+UI flow (`tests/apitesting/`), the Page Object Model in `pages/`, and the pytest-bdd suite (`tests/bdd/` + `features/`). Targets are the public practice sites at rahulshettyacademy.com, so tests need network access.

## Commands

Run everything from the repo root: `pytest.ini` sets `testpaths`, registers markers (`--strict-markers` is on) and writes reports under `reports/` relative to the current directory. There is no root `conftest.py`; imports like `from Utils...` / `from pages...` rely on pytest's rootdir-based `sys.path` insertion, since `tests/` is a package.

```bash
pip install -r requirements.txt
python -m playwright install

python -m pytest -m "smoke or regression" -n auto            # what Jenkins runs (excludes demos)
python -m pytest -m demo                                      # only the learning demos
python -m pytest tests/apitesting/test_web_api.py             # one file
python -m pytest "tests/demos/locators/test_builtin_locators.py::test_addToCard"   # one test
python -m pytest tests/apitesting --browser_name firefox      # custom option: chrome (default) | firefox | webkit
```

- `--browser_name` is a custom option defined in `tests/conftest.py` and only affects the `browser_instance` fixture. Valid values: `chrome`/`chromium`, `firefox`, `webkit`. Tests that use pytest-playwright's built-in `page` fixture (e.g. the BDD suite) are controlled by pytest-playwright's own `--browser` / `--headed` flags instead.
- Markers: `smoke`, `regression`, `demo` (registered in `pytest.ini`). BDD scenarios get markers from tags in `features/login.feature`. New framework tests need `smoke` or `regression` to run in CI.
- `requirements.txt` lists direct dependencies only (UTF-8). If PowerShell regenerates it, re-save as UTF-8.

## Architecture

- **Config/data loading** — `Utils/config_reader.py` loads `config/settings.json` at import time; tests call `get_url(name)` with keys under `urls` (`base_url`, `order_mgmt_url`, `staging`, `production`). `Utils/data_reader.py` loads `data/credentials.json` (gitignored — copy `data/credentials.example.json`, or set `TEST_CREDENTIALS_FILE`; a user record may set `"valid": false` for negative login cases); `get_users()` returns the `user_credentials` list that tests feed into `@pytest.mark.parametrize("user_credentials", ...)`.
- **Fixtures** (`tests/conftest.py`) — `browser_instance` launches a headless browser per `--browser_name` and yields a `Page` (not a browser). `api_utils` is a session-scoped `APIUtils`.
- **API layer** (`Utils/APIUtils.py`) — uses Playwright's `request.new_context` against `order_mgmt_url`. Logs in via `/api/ecom/auth/login`, caches the JWT on the instance, and creates orders via `/api/ecom/order/create-order`. Gotcha: the API expects the raw token in `Authorization`, **not** `Bearer <token>`.
- **Page Object chain** (`pages/`) — classes are lowercase and each navigation method returns the next page object: `loginpage.login()` → `dashboardpage.navigate()` → `orderhistorypage.get_order(id)` → `orderdetailspage.verif_order_details(id)`. `test_web_api.py` is the end-to-end example: create order via API, then verify it through the UI.
- **BDD** — `tests/bdd/test_login.py` binds scenarios from `features/login.feature` using an absolute path computed from the project root, and uses pytest-playwright's `page` fixture.

## Reports and CI

`pytest.ini` addopts produce `reports/junit.xml`, `reports/report.html` (pytest-html, self-contained) and, for failures, Playwright traces/screenshots in `reports/test-results/`. Traces and screenshots only cover tests using pytest-playwright's `page` fixture, not `browser_instance`. `reports/` is gitignored. pytest-html-plus was dropped; if it is still installed in an old venv it keeps writing `report_output/` (also gitignored) — `pip uninstall pytest-html-plus`.

`Jenkinsfile` (Windows agent, Pipeline-from-SCM job) creates a `.venv`, takes `BROWSER` / `MARKERS` / `WORKERS` parameters, injects test data from a Jenkins secret-file credential `playwright-test-credentials` as `TEST_CREDENTIALS_FILE`, publishes `reports/junit.xml` and archives `reports/**`.
