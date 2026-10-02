import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from Utils.data_reader import get_users

# project_root = Path('D:\\Projects\\Coding\\Playwright\\PlaywrightTraining')
#
# # Construct the path to the credentials file
# file_path = project_root / 'data' / 'credentials.json'
#
# # Check if it's a file and exists
# if not file_path.is_file():
#     raise FileNotFoundError(f"Credentials file not found at {file_path}")
#
# # Open the file
# with open(file_path, 'r') as f:
#     credentials = json.load(f)
# with open(file_path, 'r') as f:
#     credentials_list = json.load(f)


@pytest.mark.smoke
@pytest.mark.parametrize('users',get_users())
def test_login(page: Page, users):
    login_page = LoginPage(page).open()
    login_page.login(users["username"], users["password"])
    # Each user record states its expected outcome; users are valid unless marked "valid": false
    if users.get("valid", True):
        expect(page).to_have_url(DashboardPage.URL_PATTERN)
    else:
        expect(login_page.toast).to_contain_text("Incorrect email or password.")

#Add parameterized login test for multiple user credentials

#- Implemented data-driven login test using pytest and Playwright
#- Loaded test data from credentials.json file
#- Added @pytest.mark.parametrize to test multiple user logins
#- Validated login functionality for each user credential set
#- Included assertions to verify successful authentication