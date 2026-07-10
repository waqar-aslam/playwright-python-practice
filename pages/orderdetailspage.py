from playwright.sync_api import expect


class OrderDetails:
    def __init__(self, page):
        self.page = page

    def verif_order_details(self,order_id):
        expect(self.page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")
        print("✅ Test passed! Order verified successfully.")