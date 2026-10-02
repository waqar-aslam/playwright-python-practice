# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Playwright + Python (pytest) learning/practice repo. The standalone concept demos (locators, alerts, windows, frames, web tables, fixtures) live under `tests/demos/` and are auto-marked `demo` by `tests/demos/conftest.py`. The framework pieces are the API+UI flow (`tests/apitesting/`), the Page Object Model in `pages/`, and the pytest-bdd suite (`tests/bdd/` + `features/`). Targets are the public practice sites at rahulshettyacademy.com, so tests need network access.

## Commands

Run everything from the repo root: `pytest.ini` sets `testpaths`, registers markers (`--strict-markers` is on) and writes reports under `reports/` relative to the current directory. There is no root `conftest.py`; imports like `from Utils...` / `from pages...` rely on pytest's rootdir-based `sys.path` insertion, since `tests/` is a package.

```bash
pip install -r requirements-dev.txt                           # requirements.txt + ruff, pre-commit
python -m playwright install
pre-commit install                                            # ruff check --fix + ruff format on commit

python -m pytest -m "smoke or regression" -n auto            # what Jenkins runs (excludes demos)
python -m pytest -m demo                                      # only the learning demos
python -m pytest tests/apitesting/test_web_api.py             # one file
python -m pytest "tests/demos/locators/test_builtin_locators.py::test_addToCard"   # one test
python -m pytest --reruns 2                                   # pytest-rerunfailures (CI uses its RERUNS param)
ruff check . && ruff format --check .                         # lint, same as the Jenkins Lint stage
python -m pytest tests/apitesting --browser firefox --headed  # pytest-playwright flags
python -m pytest --env dev                                    # config/<env>.json (default: $TEST_ENV or dev)
python -m pytest -m smoke --log-cli-level=INFO                # stream logs to the console
```

- Every test gets its browser from pytest-playwright's `page` fixture (headless by default), so `--browser`, `--headed`, `--slowmo` and the tracing/screenshot options apply everywhere. There is no custom browser fixture.
- Markers: `smoke`, `regression`, `demo` (registered in `pytest.ini`). BDD scenarios get markers from tags in `features/login.feature`. New framework tests need `smoke` or `regression` to run in CI.
- `requirements.txt` lists direct dependencies only (UTF-8); dev tooling is in `requirements-dev.txt`. If PowerShell regenerates either, re-save as UTF-8.
- Lint/format config is `ruff.toml` (line length 120; rules E, W, F, I, B). CI fails on lint or format differences.
- Every test directory is a package (has `__init__.py`), so module names are unique (e.g. `tests.apitesting.test_login` vs `tests.bdd.test_login`). Keep it that way when adding folders.
- Don't name a fixture `browser_name`: pytest-playwright parametrizes that name and overrides it.

## Architecture

- **Config/environments** — one JSON per environment in `config/` (`dev.json` holds `base_url` and `api_base_url`). `tests/conftest.py` adds `--env` (default `$TEST_ENV` or `dev`), loads the file in `pytest_configure`, exposes it as the session `env_config` fixture, and sets pytest-base-url's `base_url` unless `--base-url` was passed. pytest-playwright gives every context that `base_url`, so page objects and tests use relative paths (`page.goto("/client/")`). A context you create yourself needs `base_url=base_url` passed in. To add an environment, add `config/<name>.json` (and the Jenkins `ENVIRONMENT` choice).
- **Test data** — `Utils/data_reader.py` loads `data/credentials.json` (gitignored — copy `data/credentials.example.json`, or set `TEST_CREDENTIALS_FILE`; a user record may set `"valid": false` for negative login cases); `get_users()` returns the `user_credentials` list that tests feed into `@pytest.mark.parametrize("user_credentials", ...)`; `get_valid_user()` returns the first user not marked invalid. The `/loginpagePractise/` demos don't use this file: `PracticeLoginPage.published_credentials()` reads the demo login the page prints.
- **Fixtures** (`tests/conftest.py`) — `env_config` (session) and `api_utils`, a session-scoped `APIUtils` that caches one token per user.
- **API layer** (`Utils/APIUtils.py`) — uses Playwright's `request.new_context` against `api_base_url`. Logs in via `/api/ecom/auth/login`, caches the JWT per user, looks up a product id via `/api/ecom/product/get-all-products` (by name, or the first listed), and creates orders via `/api/ecom/order/create-order`. Gotcha: the API expects the raw token in `Authorization`, **not** `Bearer <token>`.
- **Page objects** (`pages/`) — snake_case modules, PascalCase classes. Each class takes a `Page`, builds its locators as attributes in `__init__`, and holds its relative `URL` (opened with `open()`) or a `URL_PATTERN` for asserting. Navigation methods return the next page object: `LoginPage.login()` → `DashboardPage.go_to_orders()` → `OrderHistoryPage.view_order(id)` → `OrderDetailsPage.verify_order_details(id)`. `PracticeLoginPage` → `ShopPage` and `AutomationPracticePage` cover the practice screens the demos use. `test_web_api.py` is the end-to-end example: create order via API, then verify it through the UI.
- **Waits** — rely on auto-waiting and web-first `expect(...)` assertions; don't add `wait_for_timeout` or `networkidle`.
- **BDD** — `tests/bdd/test_login.py` binds scenarios from `features/login.feature` using an absolute path computed from the project root, and its steps go through `LoginPage` / `DashboardPage` via `login_page` / `dashboard_page` fixtures defined in that module.

## Reports and CI

`pytest.ini` addopts produce `reports/junit.xml`, `reports/report.html` (pytest-html, self-contained) and, for failures, Playwright traces/screenshots in `reports/test-results/`. Logging uses the `logging` module (`logging.getLogger(__name__)`), not `print`; pytest captures it into the report and writes `reports/pytest.log` (one `reports/pytest_gwN.log` per xdist worker). `reports/` is gitignored. pytest-html-plus was dropped; if it is still installed in an old venv it keeps writing `report_output/` (also gitignored) — `pip uninstall pytest-html-plus`.

`Jenkinsfile` (Windows agent, Pipeline-from-SCM job) creates a `.venv`, has a Lint stage (ruff), takes `BROWSER` / `ENVIRONMENT` / `MARKERS` / `WORKERS` / `RERUNS` parameters, injects test data from a Jenkins secret-file credential `playwright-test-credentials` as `TEST_CREDENTIALS_FILE`, publishes `reports/junit.xml` and archives `reports/**`.
