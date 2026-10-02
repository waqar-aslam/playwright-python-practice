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
import logging

from playwright.sync_api import Playwright

logger = logging.getLogger(__name__)


class APIUtils:
    def __init__(self, playwright: Playwright, base_url):
        """Initialize APIUtils with playwright instance and the API host"""
        self.playwright = playwright
        self.base_url = base_url
        self._tokens = {}  # username -> token, so a shared instance never reuses another user's token

    def get_access_token(self, user_credentials):
        """Return a token for this user, logging in only on first use."""
        username = user_credentials["username"]
        if username in self._tokens:
            return self._tokens[username]

        api_context = self.playwright.request.new_context(
            base_url=self.base_url,
            extra_http_headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        try:
            logger.info("API login for %s", username)
            response = api_context.post(
                "/api/ecom/auth/login",
                data={
                    "userEmail": username,
                    "userPassword": user_credentials["password"]
                }
            )
            assert response.ok, f"Login failed for {username}: HTTP {response.status} {response.text()}"
            token = response.json()["token"]
        finally:
            api_context.dispose()

        self._tokens[username] = token
        return token

    def place_order(self, user_credentials):
        """Place an order using the user's token and return the order id."""
        token = self.get_access_token(user_credentials)

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

        try:
            response = api_context.post(
                "/api/ecom/order/create-order",
                data=payload
            )
            assert response.status == 201, f"Order creation failed: HTTP {response.status} {response.text()}"
            order_id = response.json()["orders"][0]
        finally:
            api_context.dispose()

        logger.info("Order placed: %s", order_id)
        return order_id
