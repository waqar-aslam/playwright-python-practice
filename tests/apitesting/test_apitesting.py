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

from playwright.sync_api import Playwright
from pyexpat.errors import messages

BASE_URL = "https://rahulshettyacademy.com"



class TestApiTesting:



    #Helper method to get token
    def get_access_token(self,playwright: Playwright):

                # Create API context
                api_context = playwright.request.new_context(
                    base_url=BASE_URL,
                    extra_http_headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                )

                # Login payload
                login_payload = {
                    "userEmail": "aslamwaqar313@gmail.com",
                    "userPassword": "Password@11"
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

                # Extract token
                self.access_token = response_json["token"]

                print("Access Token Received:")

                api_context.dispose()

                return self.access_token

        # Call the function


    def test_place_order(self,playwright: Playwright):
        token = self.get_access_token(playwright)
        api_context = playwright.request.new_context(base_url=BASE_URL,
                                       extra_http_headers={
                                           "Authorization": token,
                                           "Content-Type": "application/json",
                                           "Accept": "application/json"
                                       })

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

        assert response.status == 201

        response_json = response.json()
        order_id = response_json["orders"][0]
        product_id = response_json["productOrderId"][0]
        message = response_json["message"][2]

