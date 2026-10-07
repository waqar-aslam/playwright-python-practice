import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "admin'--",
    "' OR 1=1; --",
    '" OR ""="',
]
XSS_PAYLOAD = "<img src=x onerror=window.__xss=true>"


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.mark.regression
@pytest.mark.parametrize("payload", INJECTION_PAYLOADS)
def test_sql_injection_does_not_log_in(page: Page, login_page: LoginPage, payload):
    login_page.enter_credentials(payload, payload)
    login_page.submit()
    expect(page).not_to_have_url(DashboardPage.URL_PATTERN)
    expect(login_page.login_button).to_be_visible()


@pytest.mark.regression
def test_xss_payload_is_not_executed(page: Page, login_page: LoginPage):
    login_page.enter_credentials(XSS_PAYLOAD, "Wrong@123")
    login_page.submit()
    expect(page).not_to_have_url(DashboardPage.URL_PATTERN)
    assert page.evaluate("window.__xss") is None
    expect(page.locator("img[src='x']")).to_have_count(0)


@pytest.mark.regression
def test_password_field_is_masked(login_page: LoginPage):
    login_page.password_input.fill("Test@123")
    expect(login_page.password_input).to_have_attribute("type", "password")


@pytest.mark.regression
def test_credentials_are_not_sent_in_url(page: Page, login_page: LoginPage):
    login_page.enter_credentials("test@wrong.com", "SecretPass@123")
    login_page.submit()
    expect(login_page.toast).to_contain_text("Incorrect email or password.")
    assert "SecretPass@123" not in page.url
    assert "test@wrong.com" not in page.url


@pytest.mark.regression
def test_failed_login_stores_no_token(page: Page, login_page: LoginPage):
    login_page.enter_credentials("test@wrong.com", "WrongPass@123")
    login_page.submit()
    expect(login_page.toast).to_contain_text("Incorrect email or password.")
    assert page.evaluate("localStorage.getItem('token')") is None


@pytest.mark.regression
def test_dashboard_requires_authentication(page: Page):
    page.goto("/client/#/dashboard/dash")
    expect(page).not_to_have_url(DashboardPage.URL_PATTERN)


@pytest.mark.regression
def test_empty_credentials_are_rejected(page: Page, login_page: LoginPage):
    login_page.submit()
    expect(login_page.email_error).to_be_visible()
    expect(login_page.password_error).to_be_visible()
    expect(page).not_to_have_url(DashboardPage.URL_PATTERN)
