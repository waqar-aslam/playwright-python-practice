from playwright.sync_api import Page, Playwright, expect


# Using the pytest-playwright `page` fixture: browser/context lifecycle is handled for you.
# Run with --headed (and optionally --slowmo 200) to watch it.
def test_bootswatch_controls(page: Page):
    page.goto("https://bootswatch.com/default/")
    expect(page.get_by_role("heading", name='Navbars')).to_be_visible()
    page.get_by_role("button", name='Primary').first.click()
    page.get_by_role("button", name='Primary').nth(2).click()
    page.get_by_role("checkbox", name='Checkbox 1').check()
    page.get_by_text(text="Radio 2").click()


# Launching manually from the `playwright` fixture: you own the lifecycle, so close what you open.
def test_open_browser_manually(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page).to_have_title("Practice Page")
    context.close()
    browser.close()
