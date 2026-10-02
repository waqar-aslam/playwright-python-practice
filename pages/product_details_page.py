import re

from playwright.sync_api import Page


class ProductDetailsPage:
    URL_PATTERN = re.compile(r".*/dashboard/product-details/\w+")

    def __init__(self, page: Page):
        self.page = page
        self.name = page.locator("h2")
        self.add_to_cart_button = page.get_by_role("button", name="Add to Cart")
        self.continue_shopping_link = page.get_by_text("Continue Shopping")

    def price(self, amount):
        return self.page.get_by_text(f"$ {amount}", exact=True)

    def continue_shopping(self):
        from pages.dashboard_page import DashboardPage  # dashboard_page imports this module

        self.continue_shopping_link.click()
        return DashboardPage(self.page)
