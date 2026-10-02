import os
import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenario, then, when

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from Utils.data_reader import get_valid_user

# Get the project root dynamically
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FEATURE_FILE = os.path.join(PROJECT_ROOT, "features", "login.feature")

# Verify the file exists
if not os.path.exists(FEATURE_FILE):
    raise FileNotFoundError(f"Feature file not found at: {FEATURE_FILE}")


# ---------- Scenarios (Feature file bindings) ----------
@scenario(FEATURE_FILE, "Login with invalid credentials")
def test_login_with_invalid_credentials():
    pass


@scenario(FEATURE_FILE, "Login with empty fields")
def test_login_with_empty_fields():
    pass


@scenario(FEATURE_FILE, "Navigate to registration page")
def test_navigate_to_registration_page():
    pass


@scenario(FEATURE_FILE, "Verify password masking")
def test_verify_password_masking():
    pass


@scenario(FEATURE_FILE, "Successful login and dashboard access")
def test_successful_login_and_dashboard_access():
    pass


# ---------- Fixtures ----------
@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page):
    return DashboardPage(page)


# ---------- Given Steps ----------
@given("the application is open")
def application_is_open(page: Page, login_page: LoginPage):
    """Navigate to the login page"""
    login_page.open()
    expect(page).to_have_url(re.compile(r".*auth/login.*"))


# ---------- When Steps ----------
@when(parsers.parse('User enters invalid email "{email}" and password "{password}"'))
def user_enters_invalid_credentials(login_page: LoginPage, email: str, password: str):
    """Enter invalid email and password"""
    login_page.enter_credentials(email, password)


@when("User clicks on the login button")
def user_clicks_login_button(login_page: LoginPage):
    """Click the login button"""
    login_page.submit()


@when("User leaves the email field empty and password field empty")
def user_leaves_fields_empty(login_page: LoginPage):
    """Ensure email and password fields are empty"""
    login_page.enter_credentials("", "")


@when(parsers.parse('User clicks on the "{link_text}" link'))
def user_clicks_register_link(login_page: LoginPage, link_text: str):
    """Click on the registration link"""
    expect(login_page.register_link).to_contain_text(link_text)
    login_page.register_link.click()


@when(parsers.parse('User enters password "{password}" in the password field'))
def user_enters_password(login_page: LoginPage, password: str):
    """Enter password in password field"""
    login_page.password_input.fill(password)


@when("User enters valid credentials from the test data")
def user_enters_valid_credentials(login_page: LoginPage):
    """Enter the first valid user from the (gitignored) test data file"""
    user = get_valid_user()
    login_page.enter_credentials(user["username"], user["password"])


# ---------- Then Steps ----------
@then(parsers.parse('User should see an error message "{expected_message}"'))
def user_sees_error_message(login_page: LoginPage, expected_message: str):
    """Verify the error toast shows the expected message (expect retries until it appears)"""
    expect(login_page.toast).to_contain_text(expected_message)


@then("User should see validation messages for both fields")
def user_sees_validation_messages(login_page: LoginPage):
    """Verify the inline 'required' message under each field"""
    expect(login_page.email_error).to_have_text("*Email is required")
    expect(login_page.password_error).to_have_text("*Password is required")


@then("The login should not be successful")
def login_not_successful(page: Page):
    """Verify user is still on login page"""
    expect(page).to_have_url(re.compile(r".*auth/login.*"))


@then("User should be redirected to the registration page")
def user_redirected_to_registration(page: Page):
    """Verify redirect to registration page"""
    expect(page).to_have_url(re.compile(r".*/auth/register.*"))


@then(parsers.parse('The URL should contain "{expected_url_part}"'))
def url_contains_text(page: Page, expected_url_part: str):
    """Verify URL contains specific text"""
    expect(page).to_have_url(re.compile(re.escape(expected_url_part)))


@then("The password should be displayed as dots or asterisks")
def password_displayed_as_dots(login_page: LoginPage):
    """Verify password is masked"""
    expect(login_page.password_input).to_have_attribute("type", "password")


@then("The password value should not be visible as plain text")
def password_not_visible_plain_text(login_page: LoginPage):
    """Verify the value is kept but the field stays masked"""
    expect(login_page.password_input).to_have_value("Test@123")
    expect(login_page.password_input).to_have_attribute("type", "password")


@then("User should be redirected to the dashboard page")
def user_redirected_to_dashboard(page: Page):
    """Verify redirect to dashboard"""
    expect(page).to_have_url(DashboardPage.URL_PATTERN)


@then(parsers.parse('The dashboard should display "{expected_text_1}" and "{expected_text_2}" navigation links'))
def dashboard_displays_sections(dashboard_page: DashboardPage, expected_text_1: str, expected_text_2: str):
    """Verify the dashboard sidebar shows the expected navigation text"""
    for text in (expected_text_1, expected_text_2):
        expect(dashboard_page.sidebar).to_contain_text(text)
