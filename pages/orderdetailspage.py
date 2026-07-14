from playwright.sync_api import expect


# Step 5: Verify success message
# print("\n=== Verifying Order Details ===")
# expect(page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")
# print("✅ Test passed! Order verified successfully.")
# page.get_by_role("button", name="Sign Out").click()


class orderdetailspage:
    def __init__(self, page):
        self.page = page

    def verif_order_details(self,order_id):
        expect(self.page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")
        print("✅ Test passed! Order verified successfully.")