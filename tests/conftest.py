import pytest
from playwright.sync_api import Playwright
from Utils.APIUtils import APIUtils

# Following import is from doc

# Project/tests/conftest.py


@pytest.fixture(scope="session")
def api_utils(playwright: Playwright):
    """Fixture to provide APIUtils instance with playwright"""
    return APIUtils(playwright)

@pytest.fixture
def user_credentials(request):
        return user_credentials
        #return credentials

def pytest_addoption(parser):
    """Add command line option for browser selection"""
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Browser to run tests: chromium, firefox, webkit"
    )

@pytest.fixture
def browser_instance(playwright,request):
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=True)
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=True)
    #elif browser_name == "chrome":

    browser_context = browser.new_context()
    page = browser_context.new_page()
    yield page
    browser_context.close()
    browser.close()

#Following code is Generated from AI deep seek
#Project/tests/conftest.py




