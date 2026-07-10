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

@pytest.fixture
def browser_instance(playwright,request):
    browser_name = request.config.getoption("--browser")
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    else:
        browser = playwright.chromium.launch(headless=False)

    browser_context = browser.new_context()
    page = browser_context.new_page()
    yield page
    browser_context.close()
    browser.close()

#Following code is Generated from AI deep seek
#Project/tests/conftest.py



# def pytest_addoption(parser):
#     """Add command line option for browser selection"""
#     parser.addoption(
#         "--browser",
#         action="store",
#         default="chromium",
#         help="Browser to run tests: chromium, firefox, webkit"
#     )
