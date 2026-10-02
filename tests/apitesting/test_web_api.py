import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from Utils.data_reader import get_users

"""
Test the complete API workflow:
1. Place an order using API
2. Navigate to the order page
3. Find and view the order
4. Verify the order details
"""


@pytest.mark.regression
@pytest.mark.parametrize("user_credentials", get_users())
def test_web_api(page: Page, api_utils, user_credentials):
    order_id = api_utils.place_order(user_credentials)

    dashboard = LoginPage(page).open().login(user_credentials["username"], user_credentials["password"])
    order_history = dashboard.go_to_orders()
    order_details = order_history.view_order(order_id)
    order_details.verify_order_details(order_id)
