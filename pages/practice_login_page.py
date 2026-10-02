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
        self.free_access_link = page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material")

    def open(self):
        self.page.goto(self.URL)
        return self

    def login(self, username, password, role="Teacher", accept_terms=False):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.role_select.select_option(role)
        if accept_terms:
            self.terms_checkbox.check()
        self.sign_in_button.click()
        return ShopPage(self.page)
