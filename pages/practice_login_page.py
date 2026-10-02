import re

from playwright.sync_api import Page

from pages.shop_page import ShopPage


class PracticeLoginPage:
    """The standalone /loginpagePractise/ login form."""

    URL = "/loginpagePractise/"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_label("Username:")
        self.password_input = page.get_by_label("Password:")
        self.role_select = page.get_by_role("combobox")
        self.terms_checkbox = page.get_by_role("checkbox", name="terms")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        # The page prints its own demo login: "(username is <user> and Password is <password>)"
        self.credentials_hint = page.locator("p", has_text="username is")
        self.free_access_link = page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material")

    def open(self):
        self.page.goto(self.URL)
        return self

    def published_credentials(self):
        """Return the (username, password) the page displays, so tests don't depend on stored data."""
        match = re.search(r"username is (\S+)\s+and\s+Password is ([^\s)]+)", self.credentials_hint.inner_text())
        assert match, "Credentials hint not found on the practice login page"
        return match.group(1), match.group(2)

    def login(self, username, password, role="Teacher", accept_terms=False):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.role_select.select_option(role)
        if accept_terms:
            self.terms_checkbox.check()
        self.sign_in_button.click()
        return ShopPage(self.page)
