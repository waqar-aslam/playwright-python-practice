# Playwright with Python - Automation Practice

A Playwright + pytest project that started as a set of learning exercises and grew into a small test framework. It
targets the public practice sites at [rahulshettyacademy.com](https://rahulshettyacademy.com), so the tests need network
access.

- **Framework tests** — page objects, API-then-UI end-to-end flow, data-driven login and a pytest-bdd suite. These run
  in CI (`smoke` / `regression` markers).
- **Demos** — one file per Playwright concept (locators, alerts, child windows, frames, web tables, fixtures, browser
  launch) under `tests/demos/`, auto-marked `demo` and excluded from CI.

## Tech stack

Python 3.12, Playwright, pytest, pytest-playwright, pytest-bdd, pytest-xdist, pytest-html, pytest-rerunfailures, ruff,
Jenkins.

## Project structure

```
PlaywrightTraining/
├── config/                 # one JSON per environment (dev.json), picked with --env
├── data/                   # test users: credentials.json is gitignored, copy credentials.example.json
├── features/               # Gherkin feature files for pytest-bdd
├── pages/                  # page objects (LoginPage, DashboardPage, OrderHistoryPage, ...)
├── Utils/                  # APIUtils (API login / product lookup / order), config and data readers
├── tests/
│   ├── conftest.py         # --env option, base_url, env_config and api_utils fixtures
│   ├── apitesting/         # data-driven login + create order via API, verify in UI
│   ├── bdd/                # step definitions for features/login.feature
│   └── demos/              # learning demos (marker: demo)
├── pytest.ini              # markers, report/trace/log settings
├── ruff.toml               # lint + format rules
├── .pre-commit-config.yaml
├── requirements.txt        # runtime/test dependencies
├── requirements-dev.txt    # + ruff and pre-commit
└── Jenkinsfile
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements-dev.txt
python -m playwright install
pre-commit install                # run ruff on every commit
```

Test users are not committed. Copy `data/credentials.example.json` to `data/credentials.json` and fill in accounts
registered on https://rahulshettyacademy.com/client (or point `TEST_CREDENTIALS_FILE` at another file). Mark a user
`"valid": false` to use it as a negative login case.

## Running tests

Run from the repo root (report paths in `pytest.ini` are relative to it).

```bash
pytest                                      # everything
pytest -m "smoke or regression" -n auto     # what CI runs, in parallel
pytest -m smoke                             # quick check
pytest -m demo                              # only the learning demos
pytest tests/apitesting/test_web_api.py     # one file
pytest --browser firefox --headed           # another browser, visible
pytest --env dev                            # config/<env>.json (default: $TEST_ENV or dev)
pytest --reruns 2                           # retry failures (live sites can be slow)
pytest -m smoke --log-cli-level=INFO        # stream logs to the console
```

## Reports

Every run writes to `reports/` (gitignored):

- `report.html` — self-contained HTML report with captured logs
- `junit.xml` — for CI test trends
- `test-results/` — Playwright trace and screenshot for each failed test (`playwright show-trace <trace.zip>`)
- `pytest.log` — log file (`pytest_gwN.log` per worker when running with `-n`)

## Linting

```bash
ruff check .          # lint (unused imports, bare except, import order, ...)
ruff format .         # format
pre-commit run --all-files
```

## CI

`Jenkinsfile` (Windows agent, "Pipeline script from SCM" job) creates a virtualenv, lints, installs the chosen browser
and runs `pytest -m "<MARKERS>" -n <WORKERS> --reruns <RERUNS>` with parameters for browser, environment, markers,
workers and reruns. Test users come from a Jenkins secret-file credential `playwright-test-credentials`. It publishes
`reports/junit.xml` and archives `reports/**`.

## Author

**Waqar Aslam** — Lead QA Automation Engineer
