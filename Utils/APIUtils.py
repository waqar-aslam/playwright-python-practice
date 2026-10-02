# Utils/APIUtils.py
# ============================================================
# API Testing Workflow
# ------------------------------------------------------------
# Step 1: Authenticate user and obtain JWT access token.
# Step 2: Store the token for subsequent API calls.
# Step 3: Use the token in the Authorization header.
# Step 4: Look up a product id (by name, or the first listed).
# Step 5: Send the Create Order POST request.
# Step 6: Verify the response status and response payload.
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

    def _new_context(self, token=None):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if token:
            headers["Authorization"] = token  # No "Bearer " prefix
        return self.playwright.request.new_context(base_url=self.base_url, extra_http_headers=headers)

    def get_access_token(self, user_credentials):
        """Return a token for this user, logging in only on first use."""
        username = user_credentials["username"]
        if username in self._tokens:
            return self._tokens[username]

        api_context = self._new_context()
        try:
            logger.info("API login for %s", username)
            response = api_context.post(
                "/api/ecom/auth/login",
                data={"userEmail": username, "userPassword": user_credentials["password"]},
            )
            assert response.ok, f"Login failed for {username}: HTTP {response.status} {response.text()}"
            token = response.json()["token"]
        finally:
            api_context.dispose()

        self._tokens[username] = token
        return token

    def get_products(self, user_credentials):
        """Return the full product catalogue (unfiltered), as the dashboard sees it."""
        api_context = self._new_context(self.get_access_token(user_credentials))
        try:
            response = api_context.post("/api/ecom/product/get-all-products", data={})
            assert response.ok, f"Product lookup failed: HTTP {response.status} {response.text()}"
            return response.json()["data"]
        finally:
            api_context.dispose()

    def get_product_id(self, user_credentials, product_name=None):
        """Return the id of the named product, or of the first listed product if no name is given."""
        products = self.get_products(user_credentials)
        if product_name is None:
            assert products, "No products available to order"
            product = products[0]
        else:
            product = next((p for p in products if p["productName"] == product_name), None)
            assert product, f"Product {product_name!r} not found; available: {[p['productName'] for p in products]}"
        logger.info("Using product %s (%s)", product["productName"], product["_id"])
        return product["_id"]

    def place_order(self, user_credentials, product_name=None, country="India"):
        """Place an order for one product and return the order id."""
        product_id = self.get_product_id(user_credentials, product_name)
        api_context = self._new_context(self.get_access_token(user_credentials))
        try:
            response = api_context.post(
                "/api/ecom/order/create-order",
                data={"orders": [{"country": country, "productOrderedId": product_id}]},
            )
            assert response.status == 201, f"Order creation failed: HTTP {response.status} {response.text()}"
            order_id = response.json()["orders"][0]
        finally:
            api_context.dispose()

        logger.info("Order placed: %s", order_id)
        return order_id
