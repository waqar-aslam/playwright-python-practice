# Utils/APIUtils.py
# ============================================================
# API Testing Workflow
# ------------------------------------------------------------
# Step 1: Authenticate user and obtain JWT access token.
# Step 2: Store the token for subsequent API calls.
# Step 3: Use the token in the Authorization header.
# Step 4: Send the Create Order POST request.
# Step 5: Verify the response status and response payload.
#
# Note:
# This API expects the raw JWT token in the Authorization
# header (not "Bearer <token>").
# ============================================================
import pytest
from playwright.sync_api import Playwright

BASE_URL = "https://rahulshettyacademy.com"


class APIUtils:
    def __init__(self, playwright: Playwright):
        """Initialize APIUtils with playwright instance"""
        self.playwright = playwright
        self.base_url = BASE_URL
        self.access_token = None  # Store token for reuse

    def get_access_token(self,user_credentials):
        """Helper method to get token - only logs in if token doesn't exist"""
        # If token already exists, return it (no new login)
        if self.access_token:
            print("🔄 Using existing token (no login needed)")
            return self.access_token

        print("🔐 Logging in to get new token...")
        print(user_credentials["username"])
        print(user_credentials["password"])

        # Create API context
        api_context = self.playwright.request.new_context(
            base_url=self.base_url,
            extra_http_headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        # Login payload
        login_payload = {
            "userEmail": user_credentials["username"],
            "userPassword": user_credentials["password"]
        }

        # Send POST request to login endpoint
        response = api_context.post(
            "/api/ecom/auth/login",
            data=login_payload
        )

        # Validate response
        assert response.ok, f"Login failed: {response.status}"

        # Convert response to JSON
        response_json = response.json()

        # Extract and store token
        self.access_token = response_json["token"]
        print("✅ Access Token Received and Stored")

        api_context.dispose()
        return self.access_token

    def place_order(self,user_credentials):
        """Place an order using the stored token"""
        # Get token (will reuse existing token if available)
        token = self.get_access_token(user_credentials)
        print(f"Using token for order: {token[:20]}...")

        api_context = self.playwright.request.new_context(
            base_url=self.base_url,
            extra_http_headers={
                "Authorization": token,  # No "Bearer " prefix
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        payload = {
            "orders": [
                {
                    "country": "India",
                    "productOrderedId": "6960eae1c941646b7a8b3ed3"
                }
            ]
        }

        response = api_context.post(
            "/api/ecom/order/create-order",
            data=payload
        )

        print("Status Code:", response.status)
        print("Response Body:", response.text())

        assert response.status == 201, f"Order creation failed: {response.status}"

        response_json = response.json()
        order_id = response_json["orders"][0]
        print(f"✅ Order placed successfully! Order ID: {order_id}")

        api_context.dispose()
        return order_id