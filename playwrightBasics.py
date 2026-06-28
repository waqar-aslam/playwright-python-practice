from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import Playwright
def test_openBrowser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.close()
    context.close()

def test_openBrowser2(page: Page,playwright: Playwright):
    browser =playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.close()


def test_openBrowser3(page: Page,playwright: Playwright):
