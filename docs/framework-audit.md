# Framework audit: Playwright + pytest

> **Status:** written before any changes, against the code as it was then; line numbers refer to that version.
> The roadmap at the end has been implemented: P0 `9049630`, P1 `443e445`, P2 `4775f87`, P3 `e02bf16`.

_Audit of the Playwright + pytest framework (branch PlaywrightTraining-upgrade)_

Summary: This is a learning repo that has started turning into a framework, and the two layers are mixed together. The good parts are real: page objects that hand you the next page, setup done through an API before the UI test, data-driven tests, BDD, and config files kept separate from code. But several tests can't pass, and some pass when they shouldn't. Fixed sleeps are used throughout, passwords are committed in three places, and the CI pipeline archives a stale committed report instead of the one the run produced. Nothing below was run or changed; it all comes from reading the code.

## Ratings

| Area | Rating |
|---|---|
| Folder structure | Fair |
| Design patterns | Fair |
| Code duplication | Poor |
| Wait / synchronization | Poor |
| Test data handling | Poor |
| Configuration management | Fair |
| Reporting | Poor |
| Logging | Poor |
| Error handling | Poor |
| CI readiness | Poor |

---

## 1. Folder structure — Fair

Good: The top-level split into pages/, Utils/, config/, data/, features/ and tests/<topic>/ is the right shape.

**Problems**
- Tests that never run: pytest only collects files named test_*.py, so these are silently skipped: tests/alerts/handleAlerts.py, tests/fixtures/fixScopeDemo.py (which is entirely commented out) and tests/readingfile.py.
- Misnamed package file: tests/locators/__initi__.py has a typo, so tests/locators isn't a package. tests/bdd/ has no __init__.py either. As a result, how imports resolve differs from folder to folder.
- Two files named test_login.py (tests/apitesting/ and tests/bdd/). This only works because one folder is a package and the other isn't, and it will break the moment someone "fixes" the __init__ files.
- Generated output is committed: report_output/ in four places, .pytest_worker_jsons/ in two, report.html at the root, and manual screenshots. None of this is in .gitignore.
- Inconsistent naming: Utils/ is capitalised while the other folders aren't. APIUtils.py is CamelCase. The page classes are all lowercase (loginpage, dashboardpage).
- README is out of date: it describes tests/basics/, tests/waits/, a pytest.ini and a root conftest.py, none of which exist.
- Unused file: assets/style.css isn't referenced by any config.

## 2. Design patterns — Fair

**Good**
- The page objects hand off to each other in order (pages/loginpage.py → dashboardpage → orderhistorypage → orderdetailspage).
- The API-then-UI test (tests/apitesting/test_web_api.py) is a solid pattern.
- The pytest-bdd tests are correctly bound to features/login.feature.

**Problems**
- Page object methods take a redundant page argument even though the object already stores it: pages/loginpage.py:469 and :472 (navigate(self, page), login(self, page, ...)).
- The login URL is hard-coded in pages/loginpage.py:470 instead of coming from config.
- verif_order_details(order_id) ignores order_id (pages/orderdetailspage.py). It only checks a generic thank-you message, so it would pass for any order. The method name also has a typo.
- Tests bypass the page objects:
  - tests/locators/test_builtin_locators.py (test_tryagain4, test_addToCard), tests/apitesting/test_login.py:30-32 and the BDD steps all locate elements inline.
  - The BDD steps use different selectors (#userEmail) from loginpage (placeholders) for the same screen.
- Two different ways of getting a browser are in use:
  - The custom browser_instance fixture (tests/conftest.py:30).
  - pytest-playwright's built-in page fixture.
  - --browser_name only affects the first; --browser / --headed only affect the second.
- api_utils fixture is never used: it's session-scoped in tests/conftest.py:12, but test_web_api.py:25 creates APIUtils directly. If anyone does adopt it, the cached token is never tied to a user (Utils/APIUtils.py:371), so every user after the first would get the first user's token.
- Fixture imported directly: tests/locators/test_builtin_locators.py:7 imports from tests.conftest, so the same fixture is registered twice.

## 3. Code duplication — Poor

- Duplicate tests that check nothing: tests/locators/test_builtin_locators.py:10-31 has test_run, test_tryagain, test_tryagain2 and test_tryagain3. All four are identical (open a URL) and have no assertions.
- Login copied between tests: the same login sequence appears in test_tryagain4 (:37-43) and test_addToCard (:52-57).
- Two copies of the child-window test: test_handleChildWindow and test_handleChildWindow2 (:69-90) share the same setup.
- Two copies of the alert test: tests/alerts/handleAlerts.py duplicates test_demoHandleAlert in tests/windows/test_child_windows.py:15.
- Copy-pasted toast lookup: tests/bdd/test_login.py:676-703 repeats the same loop twice in a row.
- JSON loading written twice: tests/readingfile.py re-implements what Utils/config_reader.py and data_reader.py already do.
- One browser test written five ways: tests/browsers/test_launch_browser.py has five variants of "open a browser".
- Leftover code: about 40 lines of commented-out old code are spread across the page objects and tests (e.g. pages/dashboardpage.py:1-11, tests/apitesting/test_login.py:10-23).

## 4. Wait / synchronization strategy — Poor

Good: Most of the POM tests and the locator tests rely on Playwright's auto-waiting and expect correctly.

**Problems**
- Fixed sleeps in the BDD steps: tests/bdd/test_login.py calls wait_for_timeout at lines 613, 624, 655, 691, 763, 795, 811, 851, 861 and 862. Together that's about 7–8 s of hard-coded sleep, plus 10 s timeouts at 866–868.
- networkidle waits at tests/bdd/test_login.py:594, 632, 810, 818, 850 and 860. Playwright discourages these for single-page apps like this one.
- Popup handled inside its own with block: in tests/locators/test_builtin_locators.py:72-79 and :86-90, popup.value is read before the with page.expect_popup() block has finished. The popup isn't available yet at that point, so these tests can't work as written. There's a committed failure screenshot for test_handleChildWindow2.
- Bypasses retrying assertions: test_handleChildWindow reads the text once with .text_content() and asserts on it with a plain assert, so it doesn't retry the way expect would.
- Sleep-based polling in tests/bdd/test_login.py:676-703. A single expect(locator).to_contain_text(...) would replace it.

## 5. Test data handling — Poor

- Credentials are committed in three places:
  - data/credentials.json
  - features/login.feature:30 (a real email and password)
  - the env file at the repo root (TEST_EMAIL, TEST_PASSWORD)
  - The env file isn't loaded by anything, and it's named env, not .env.
- Credentials are printed to the output:
  - Utils/APIUtils.py:376-377 prints the username and password.
  - tests/readingfile.py:9 prints the entire credentials file.
- Expected results aren't in the data: test_login.py is parametrised over every user without saying which should succeed, so the test guesses with a try/except (see section 9).
- Data picked by position: get_users()[2] in test_builtin_locators.py:38 and :53. Reordering credentials.json silently changes what the test uses.
- Hard-coded API payload: product ID 6960eae1c941646b7a8b3ed3 and country India (Utils/APIUtils.py:432-433). The test breaks when that product is removed from the site.
- Data loaded at import: files are read with a print the moment the module is imported (Utils/data_reader.py:6). A missing file breaks collection of every test, not just the ones that need it.

## 6. Configuration management — Fair

Good: URLs are centralised in config/settings.json and read through get_url().

**Problems**
- Settings that do nothing: browser and headless in settings.json aren't read anywhere. Headless is hard-coded in tests/conftest.py:33-37. And if browser: "chromium" were wired up as it stands, it would crash the fixture.
- Browser fixture bugs (tests/conftest.py:32-37):
  - chrome is checked with its own if while firefox/webkit are an if/elif, so the chain is broken.
  - Any unrecognised name (including chromium, which the help text suggests) leaves browser undefined and crashes the fixture.
- No environment switching: there's no way to choose an environment. The keys staging and production are really just more URLs:
  - staging points at the AutomationPractice demo site.
  - production is example.com.
- URLs hard-coded in tests instead of config:
  - pages/loginpage.py:470
  - tests/bdd/test_login.py:558-559
  - tests/apitesting/test_login.py:38
  - every test in tests/windows/, tests/alerts/ and tests/webtables/
- No pytest.ini or pyproject.toml: markers, default options, the report path and the test file pattern aren't configured anywhere. pytest-base-url is installed but unused.
- Messy requirements.txt:
  - It's a full pip freeze saved as UTF-16.
  - It includes xdist==0.0.2, a different, junk package from pytest-xdist.
  - It includes utils, yagmail, keyring and pywin32-ctypes, which nothing in the code uses.

## 7. Reporting — Poor

- Two report plugins: pytest-html (report.html plus assets/style.css) and pytest-html-plus (report_output/) are both installed. Only pytest-html-plus runs by default.
- Jenkins archives a stale report:
  - The Jenkinsfile archives report.html, but pytest --tb=short never passes --html, so no new report is produced.
  - The step succeeds only because report.html is committed, so the "build report" is the same old file every time.
- Report folders scattered: report_output/ is written relative to wherever pytest is run from, which is why copies exist under tests/, tests/bdd/, tests/locators/ and tests/windows/.
- No JUnit XML: Jenkins can't show test trends or per-test history without it.
- Failure-only evidence: you only get screenshots on failure. There are no Playwright traces or videos (--tracing=retain-on-failure, which pytest-playwright supports).
- Debug screenshot written to the working directory: tests/bdd/test_login.py:747 writes error_debug.png there, outside any report.

## 8. Logging — Poor

- No logging at all: everything is print. The logging module isn't used anywhere, there are no log levels, and nothing captures a log file.
- Prints with side effects:
  - Utils/config_reader.py:9 and Utils/data_reader.py:5 print on import.
  - Utils/APIUtils.py prints secrets (376-377) and token fragments (418).
- Emoji in print statements (APIUtils.py, orderdetailspage.py). On a Windows Jenkins agent with a cp1252 console, these can raise UnicodeEncodeError.

## 9. Error handling — Poor

- BDD error check can pass for anything: "Method 5" in tests/bdd/test_login.py:737-742 sets error_found = True whenever the page is still on login. "User should see error X" passes even if no error message is shown at all.
- Login test that always passes: tests/apitesting/test_login.py:34-38 uses a bare except: to decide which outcome to check. A failed login and a passed login both count as success.
- Bare except: that swallows real failures: tests/bdd/test_login.py lines 686, 702, 733, 869 and 883. These also catch KeyboardInterrupt and assertion errors.
- Unhandled API failures: Utils/APIUtils.py:401-412.
  - The login assert is commented out, and the function returns None when login fails.
  - place_order then crashes on token[:20] with a TypeError instead of reporting "login failed: 401".
  - The API context isn't cleaned up on that failure path.
- Broken selectors: tests/locators/test_builtin_locators.py:103 and :111 use locator("left-align") and locator("openwindow"), missing the . or #, so they look for HTML tags that don't exist. There's a committed failure screenshot for this test.
- Variable that may not exist: tests/webtables/test_demoWebTables.py:16 uses price_col_value, which is never set if the "Price" header isn't found.
- Unused import: tests/alerts/handleAlerts.py:1 imports tkinter's dialog, and the lambda parameter then shadows it.

## 10. CI readiness — Poor

- Browser launched while pytest is still collecting: tests/browsers/test_launch_browser.py:5-15 starts a browser at module level. Its tests:
  - launch headless=False browsers they never close
  - shadow the page fixture (:27)
  - will fail or hang on an agent with no display
- Jenkinsfile problems:
  - It's Windows-only (bat).
  - It checks the repo out again when the pipeline has already done so.
  - It installs straight into the system Python with no virtual environment.
  - There's no browser or environment parameter, no parallel run (xdist is installed but not used), no JUnit publishing and no timeout.
- Markers not registered: @pytest.mark.smoke and @pytest.mark.regression are used but never declared. That produces warnings now, and errors under --strict-markers.
- No way to run a subset: there's no smoke/regression split, so CI runs everything, including the learning demos.
- Passwords committed (section 5), with no credential injection from Jenkins.
- Nothing isolates the external sites: every test depends on live rahulshettyacademy.com, with no retries (pytest-rerunfailures).
- No quality checks: there's no lint, formatter or type check (ruff/black/flake8), so issues like the unused imports and bare excepts above aren't caught automatically.

---

## Prioritized roadmap

### P0 — Fix things that are broken or unsafe (about 1 day)
1. Remove the committed credentials.
   - Delete the passwords from data/credentials.json, features/login.feature and env.
   - Load credentials from environment variables instead (python-dotenv locally, Jenkins credentials() in CI).
   - Change any real passwords, since they're in git history. Delete the credential-printing lines.
2. Fix the tests that can pass when they shouldn't:
   - BDD "Method 5"
   - the try/except in tests/apitesting/test_login.py (add an expected field to each user record)
   - verif_order_details (actually check the order ID)
3. Fix the broken tests:
   - Move the popup handling out of the with block.
   - Fix the selectors in test_traverse_parent_to_child.
   - Fix the browser selection chain in browser_instance and accept chromium.
4. Stop the module-level browser launch in tests/browsers/test_launch_browser.py, and remove the headless=False launches.
5. Make APIUtils fail clearly: assert that login succeeded, and tie the cached token to the user.

### P1 — Get CI trustworthy (2–3 days)
1. Add pytest.ini with:
   - testpaths
   - registered markers
   - --strict-markers
   - addopts for --junitxml, --html=reports/report.html --self-contained-html, --tracing=retain-on-failure and --screenshot=only-on-failure
2. Stop committing generated output: add report_output/, reports/, report.html and .pytest_worker_jsons/ to .gitignore and git rm --cached them. Choose one HTML report plugin.
3. Update the Jenkinsfile:
   - venv
   - parameters for browser, environment and marker
   - -n auto
   - junit publishing
   - archive the generated reports and traces
   - a timeout
4. Separate the learning demos: move them into tests/demos/ (or mark them demo) so CI runs -m "smoke or regression" only.
5. Rebuild requirements.txt as UTF-8 with direct dependencies only, and drop xdist, utils, yagmail and keyring.

### P2 — Framework structure (about a week)
1. One way to get a browser: use pytest-playwright's page/browser fixtures everywhere and drop the custom browser_instance.
2. Config by environment: sections like config/{dev,staging}.json, selected with --env or ENV=. Set base_url for pytest-base-url and use relative page.goto("/client/"). Wire up headless and browser from settings, or delete them.
3. Fix up the page objects:
   - PascalCase classes and snake_case modules.
   - Remove the extra page arguments.
   - Pull locators into class attributes.
   - Take URLs from config.
   - Add page objects for the loginpagePractise and AutomationPractice screens.
   - Have the BDD steps reuse the page objects.
4. Replace every wait_for_timeout and networkidle with web-first expect assertions, and collapse the toast-polling loops into a single expect.
5. Structured logging: use the logging module, with pytest's log_cli and log_file settings. Remove prints from module import and drop the emoji.

### P3 — Polish
1. Remove dead code: the commented-out code and the duplicate tests (test_run/tryagain*, the duplicate alert and child-window tests). Fix the __initi__.py typo and add tests/bdd/__init__.py.
2. Linting: ruff and black via pre-commit, which would have flagged most of the unused imports and bare excepts above.
3. API test data: look up a product ID through the API rather than hard-coding one, and add a pytest-rerunfailures policy for tests that depend on the live sites.
4. Rewrite the README to match the real structure and commands.
