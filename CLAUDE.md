# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Playwright + Python (pytest) learning/practice repo. Most files under `tests/` are standalone concept demos (locators, alerts, windows, frames, web tables, fixtures). The more framework-like pieces are the API+UI flow (`tests/apitesting/`), the Page Object Model in `pages/`, and the pytest-bdd suite (`tests/bdd/` + `features/`). Targets are the public practice sites at rahulshettyacademy.com, so tests need network access.

## Commands

Run everything from the repo root (there is no `pytest.ini` or root `conftest.py`; imports like `from Utils...` / `from pages...` rely on pytest's rootdir-based `sys.path` insertion, since `tests/` is a package).

```bash
pip install -r requirements.txt
python -m playwright install

python -m pytest --tb=short                                   # what Jenkins runs
python -m pytest tests/apitesting/test_web_api.py             # one file
python -m pytest "tests/locators/test_builtin_locators.py::test_addToCard"   # one test
python -m pytest tests/apitesting --browser_name firefox      # custom option: chrome (default) | firefox | webkit
python -m pytest -n 3                                         # parallel via pytest-xdist
```

- `--browser_name` is a custom option defined in `tests/conftest.py` and only affects the `browser_instance` fixture. Valid values are `chrome`, `firefox`, `webkit` — `chromium` (despite the help text) leaves `browser` unbound and errors. Tests that use pytest-playwright's built-in `page` fixture (e.g. the BDD suite) are controlled by pytest-playwright's own `--browser` / `--headed` flags instead.
- `requirements.txt` is UTF-16 encoded (written by a PowerShell redirect). pip reads it fine, but preserve the encoding or re-save deliberately when editing it.

## Architecture

- **Config/data loading** — `Utils/config_reader.py` loads `config/settings.json` at import time; tests call `get_url(name)` with keys under `urls` (`base_url`, `order_mgmt_url`, `staging`, `production`). `Utils/data_reader.py` loads `data/credentials.json`; `get_users()` returns the `user_credentials` list that tests feed into `@pytest.mark.parametrize("user_credentials", ...)`.
- **Fixtures** (`tests/conftest.py`) — `browser_instance` launches a headless browser per `--browser_name` and yields a `Page` (not a browser). `api_utils` is a session-scoped `APIUtils`.
- **API layer** (`Utils/APIUtils.py`) — uses Playwright's `request.new_context` against `order_mgmt_url`. Logs in via `/api/ecom/auth/login`, caches the JWT on the instance, and creates orders via `/api/ecom/order/create-order`. Gotcha: the API expects the raw token in `Authorization`, **not** `Bearer <token>`.
- **Page Object chain** (`pages/`) — classes are lowercase and each navigation method returns the next page object: `loginpage.login()` → `dashboardpage.navigate()` → `orderhistorypage.get_order(id)` → `orderdetailspage.verif_order_details(id)`. `test_web_api.py` is the end-to-end example: create order via API, then verify it through the UI.
- **BDD** — `tests/bdd/test_login.py` binds scenarios from `features/login.feature` using an absolute path computed from the project root, and uses pytest-playwright's `page` fixture.

## Reports

pytest-html-plus writes `report_output/` (`report.html`, `final_report.json`, `plus_metadata.json`, `screenshots/*_failure.png`) relative to the directory pytest was run from — which is why stray `report_output/` folders exist under `tests/` subdirectories. Jenkins archives `report.html` from the root. These outputs are currently committed to git, so test runs will dirty the working tree.
