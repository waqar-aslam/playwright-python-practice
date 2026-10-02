import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from Utils.data_reader import get_users


@pytest.mark.smoke
@pytest.mark.parametrize("users", get_users())
def test_login(page: Page, users):
    login_page = LoginPage(page).open()
    login_page.login(users["username"], users["password"])
    # Each user record states its expected outcome; users are valid unless marked "valid": false
    if users.get("valid", True):
        expect(page).to_have_url(DashboardPage.URL_PATTERN)
    else:
        expect(login_page.toast).to_contain_text("Incorrect email or password.")
