import pytest
from playwright.sync_api import Playwright

from Utils.APIUtils import APIUtils
from Utils.data_reader import get_users
from pages.loginpage import loginpage

user_credentials_list = get_users()

"""
Test the complete API workflow:
1. Place an order using API
2. Navigate to the order page
3. Find and view the order
4. Verify the success message
"""


@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_web_api(playwright: Playwright, browser_instance, user_credentials):
    api_utils = APIUtils(playwright)

    # Step 1: Place an order using API (only logs in once)
    print("\n=== Placing Order ===")
    order_id = api_utils.place_order(user_credentials)
    print(f"Order ID to search: {order_id}")

    username = user_credentials["username"]
    password = user_credentials["password"]
    login = loginpage(browser_instance)


    login.navigate(browser_instance)
    dashboard = login.login(browser_instance, username, password)
    order_page = dashboard.navigate()
    order_detail = order_page.get_order(order_id)
    order_detail.verif_order_details(order_id)
