from playwright.sync_api import Page, expect


class OrderDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.order_id = page.locator(".col-text")
        self.tagline = page.locator(".tagline")

    def verify_order_details(self, order_id):
        expect(self.order_id).to_have_text(order_id)
        expect(self.tagline).to_contain_text("Thank you for Shopping With Us")
