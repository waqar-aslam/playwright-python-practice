import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from Utils.config_reader import settings, get_url
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


@pytest.mark.parametrize('users',get_users())
def test_login(page: Page, users):

    page.goto(get_url("order_mgmt_url"))
    page.get_by_placeholder(text="email@example.com").fill(users["username"])
    page.get_by_placeholder(text="enter your passsword").fill(users["password"])
    page.get_by_role("button", name="login").click()
    expect(page).to_have_url("https://rahulshettyacademy.com/client/#/dashboard/dash")

#Add parameterized login test for multiple user credentials

#- Implemented data-driven login test using pytest and Playwright
#- Loaded test data from credentials.json file
#- Added @pytest.mark.parametrize to test multiple user logins
#- Validated login functionality for each user credential set
#- Included assertions to verify successful authentication