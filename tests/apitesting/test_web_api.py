# tests/apitesting/test_web_api.py
import json
import os

import pytest
from playwright.sync_api import Playwright
from Utils.APIUtils import APIUtils
from pages.loginpage import loginpage
from tests.apitesting.conftest import browser_instance

current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir = D:\Projects\Coding\Playwright\PlaywrightTraining\tests\apitesting

# Go up two levels to reach the project root
project_root = os.path.dirname(os.path.dirname(current_dir))
# project_root = D:\Projects\Coding\Playwright\PlaywrightTraining

# Build the path to credentials.json
json_path = os.path.join(project_root, "data", "credentials.json")
# json_path = D:\Projects\Coding\Playwright\PlaywrightTraining\data\credentials.json


with open(json_path, 'r') as file:
    test_data = json.load(file)
    user_credentials_list = test_data["user_credentials"]


@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_web_api(playwright: Playwright,browser_instance, user_credentials):
    # browser = playwright.chromium.launch(headless=True)
    # context = browser.new_context()
    # page = context.new_page()
    api_utils = APIUtils(playwright)
    """
    Test the complete API workflow:
    1. Place an order using API
    2. Navigate to the order page
    3. Find and view the order
    4. Verify the success message
    """

    # Get list of users from fixture

     #username = get_credentials["username"]
     #password = get_credentials["password"]

    # Step 1: Place an order using API (only logs in once)
    print("\n=== Placing Order ===")
    order_id = api_utils.place_order(user_credentials)
    print(f"Order ID to search: {order_id}")

    username = user_credentials["username"]
    password = user_credentials["password"]

    login = loginpage(browser_instance)
    login.navigate(browser_instance)
    dashboard = login.login(browser_instance, username, password)
    order_page= dashboard.navigate()
    order_detail =order_page.get_order(order_id)
    order_detail.verif_order_details(order_id)

