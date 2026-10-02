import pytest
from playwright.sync_api import Browser, Error, Page, Playwright, expect


# Using the pytest-playwright `page` fixture: browser/context lifecycle is handled for you.
# Run with --headed (and optionally --slowmo 200) to watch it.
def test_bootswatch_controls(page: Page):
    page.goto("https://bootswatch.com/default/")
    expect(page.get_by_role("heading", name="Navbars")).to_be_visible()
    page.get_by_role("button", name="Primary").first.click()
    page.get_by_role("button", name="Primary").nth(2).click()
    page.get_by_role("checkbox", name="Checkbox 1").check()
    page.get_by_text(text="Radio 2").click()


# Launching manually from the `playwright` fixture: you own the lifecycle, so close what you open.
# Contexts you create yourself don't get base_url automatically, so pass the fixture in.
def test_open_browser_manually(playwright: Playwright, base_url):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("/AutomationPractice/")
    expect(page).to_have_title("Practice Page")
    context.close()
    browser.close()


# The tests below take pytest-playwright's shared `browser` fixture and open their own contexts.
# `with browser.new_context() as context:` closes the context even when a check fails.


# Each context is a separate, incognito-like profile: storage set in one is invisible to another.
def test_contexts_are_isolated(browser: Browser, base_url):
    with browser.new_context(base_url=base_url) as first, browser.new_context(base_url=base_url) as second:
        page_a = first.new_page()
        page_a.goto("/AutomationPractice/")
        page_a.evaluate("localStorage.setItem('user', 'alice')")

        page_b = second.new_page()
        page_b.goto("/AutomationPractice/")

        assert page_a.evaluate("localStorage.getItem('user')") == "alice"
        assert page_b.evaluate("localStorage.getItem('user')") is None


# Pages (tabs) in the same context share cookies and storage, like tabs in one browser window.
def test_pages_in_one_context_share_state(browser: Browser, base_url):
    with browser.new_context(base_url=base_url) as context:
        first_tab = context.new_page()
        first_tab.goto("/AutomationPractice/")
        context.add_cookies([{"name": "session", "value": "abc123", "url": base_url}])
        first_tab.evaluate("localStorage.setItem('theme', 'dark')")

        second_tab = context.new_page()
        second_tab.goto("/AutomationPractice/")

        assert len(context.pages) == 2
        assert second_tab.evaluate("localStorage.getItem('theme')") == "dark"
        assert "session=abc123" in second_tab.evaluate("document.cookie")


# Device descriptors set viewport, user agent, touch and mobile mode in one go.
# Firefox doesn't support mobile emulation (is_mobile), so it's skipped there.
@pytest.mark.skip_browser("firefox")
def test_mobile_device_emulation(playwright: Playwright, browser: Browser, base_url):
    iphone = playwright.devices["iPhone 13"]
    with browser.new_context(**iphone, base_url=base_url) as context:
        page = context.new_page()
        page.goto("/AutomationPractice/")

        assert page.viewport_size == iphone["viewport"]
        # screen.width is the device's 390px. window.innerWidth would be ~1000: this page has no
        # <meta name="viewport">, so mobile mode lays it out at desktop width and zooms out, like a real phone.
        assert page.evaluate("screen.width") == iphone["viewport"]["width"]
        assert "iPhone" in page.evaluate("navigator.userAgent")
        assert page.evaluate("navigator.maxTouchPoints") > 0


# Locale, timezone and viewport are context options too; the page sees them through normal browser APIs.
def test_locale_timezone_and_viewport(browser: Browser):
    with browser.new_context(
        locale="fr-FR", timezone_id="Asia/Karachi", viewport={"width": 1024, "height": 640}
    ) as context:
        page = context.new_page()

        assert page.evaluate("navigator.language") == "fr-FR"
        assert page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone") == "Asia/Karachi"
        assert page.evaluate("[window.innerWidth, window.innerHeight]") == [1024, 640]
        # French number formatting proves the locale reaches Intl, not just navigator.language
        assert page.evaluate("(1234.5).toLocaleString()").replace("\u202f", " ") == "1 234,5"


# set_offline() cuts the context's network: navigation fails until it is switched back on.
def test_offline_context_blocks_navigation(browser: Browser, base_url):
    with browser.new_context(base_url=base_url) as context:
        page = context.new_page()
        context.set_offline(True)
        with pytest.raises(Error):
            page.goto("/AutomationPractice/")

        context.set_offline(False)
        page.goto("/AutomationPractice/")
        expect(page).to_have_title("Practice Page")
