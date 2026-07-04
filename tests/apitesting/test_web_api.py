# tests/apitesting/test_web_api.py
import json

import pytest
from playwright.sync_api import expect, Page
from Utils.APIUtils import APIUtils



with open("data/credentials.json", 'r') as file:
    test_data = json.load(file)
    user_credentials_list = test_data["user_credentials"]


@pytest.mark.parametrize('user_credentials',user_credentials_list)
def test_web_api(page: Page, api_utils: APIUtils,user_credentials):
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
    order_id = api_utils.place_order()
    print(f"Order ID to search: {order_id}")

    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.get_by_placeholder(text="email@example.com").fill(user_credentials["username"])
    page.get_by_placeholder(text="enter your passsword").fill(user_credentials["password"])
    page.get_by_role("button",name="Login").click()

    # Step 2: Navigate to orders page
    print("\n=== Navigating to Orders Page ===")
    page.get_by_role("button", name="ORDERS").click()

    # Step 3: Find the order in the table
    print(f"\n=== Searching for Order: {order_id} ===")
    row = page.locator("tr").filter(has_text=order_id)

    # Step 4: Click View button
    row.get_by_role("button", name="View").click()

    # Step 5: Verify success message
    print("\n=== Verifying Order Details ===")
    expect(page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")
    print("✅ Test passed! Order verified successfully.")