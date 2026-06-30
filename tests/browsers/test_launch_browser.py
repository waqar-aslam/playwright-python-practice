from playwright.sync_api import sync_playwright, expect, Playwright
from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import Playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False,slow_mo=200)
    page = browser.new_page()
    page.goto("http://bootswatch.com/default/")
    #page.get_by_role("heading",{ name: 'Navbars'}).highlight()
    expect(page.get_by_role("heading",name='Navbars')).to_be_visible();
    page.get_by_role("button",name='Primary').first.click()
    page.get_by_role("button",name='Primary').nth(2).click()
    page.get_by_role("checkbox",name='Checkbox 1').check()
    page.get_by_text(text="Radio 2").click()
    page.close()


    def test_openBrowser(playwright: Playwright):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://rahulshettyacademy.com/AutomationPractice/")
        page.close()
        context.close()


    def test_openBrowser2(page: Page, playwright: Playwright):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://rahulshettyacademy.com/client/#/auth/login")
        page.close()


    def test_open_broswer(playwright: Playwright):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://rahulshettyacademy.com/AutomationPractice/")
        page.close()
        context.close()


    def test_open_broswer2(playwright: Playwright, page: Page):
        browser = playwright.chromium.launch(headless=False)
        # context = browser.new_context()
        # page = context.new_page()
        page.goto("https://rahulshettyacademy.com/")
        page.close()
