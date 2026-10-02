from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage


class LoginPage:
    """Login screen of the e-commerce client app."""

    URL = "/client/#/auth/login"

    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("#userEmail")
        self.password_input = page.locator("#userPassword")
        self.login_button = page.locator("#login")
        self.email_error = page.locator("#userEmail + .invalid-feedback")
        self.password_error = page.locator("#userPassword + .invalid-feedback")
        self.toast = page.locator("#toast-container")
        self.register_link = page.locator("a", has_text="Register here")  # no href, so it has no link role

    def open(self):
        self.page.goto(self.URL)
        return self

    def enter_credentials(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)

    def submit(self):
        self.login_button.click()

    def login(self, email, password):
        self.enter_credentials(email, password)
        self.submit()
        return DashboardPage(self.page)
