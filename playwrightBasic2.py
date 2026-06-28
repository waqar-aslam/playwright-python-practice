from playwright.sync_api import Playwright, Page


def test_open_broswer(playwright:Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.close()
    context.close()


def test_open_broswer2(playwright:Playwright,page:Page):
    browser = playwright.chromium.launch(headless=False)
   # context = browser.new_context()
    #page = context.new_page()
    page.goto("https://rahulshettyacademy.com/")
    page.close()
