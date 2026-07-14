from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

scenarios("../../features/login.feature")

@given("the application is open")
def open_login_page(page: Page):
    page.goto("https://rahulshettyacademy.com/client/#/auth/login")

@given("the user is on the login page")
def user_on_login_page(page: Page):
    assert "rahulshettyacademy" in page.url
    #page.wait_for_selector("#username", state="visible")

# ONE function handles both username AND password
@when(parsers.parse('the user enters username "{username}" and password "{password}"'))
def enter_credentials(page: Page, username: str, password: str):
    page.get_by_placeholder("email@example.com").fill(username)
    page.get_by_placeholder("enter your passsword").fill(password)
    #print(f"Entered credentials - User: {username}")

@when("clicks the Sign In button")
def click_sign_in(page: Page):
    page.get_by_role("button").click()

@then("the dashboard should be displayed")
def verify_dashboard(page: Page):
    expect(page.get_by_text("Automation Practice")).to_be_visible()

