# tests/apitesting/test_web_api.py
from playwright.sync_api import expect, Page
from Utils.APIUtils import APIUtils


def test_web_api(page: Page, api_utils: APIUtils):
    """
    Test the complete API workflow:
    1. Place an order using API
    2. Navigate to the order page
    3. Find and view the order
    4. Verify the success message
    """


    # Step 1: Place an order using API (only logs in once)
    print("\n=== Placing Order ===")
    order_id = api_utils.place_order()
    print(f"Order ID to search: {order_id}")

    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.get_by_placeholder(text="email@example.com").fill("aslamwaqar313@gmail.com")
    page.get_by_placeholder(text="enter your passsword").fill("Password@11")
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