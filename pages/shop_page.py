import re

from playwright.sync_api import Page


class ShopPage:
    URL_PATTERN = re.compile(r".*shop")

    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator("app-card")
        self.checkout_link = page.get_by_text(re.compile(r"Checkout \( \d+ \)"))
        self.cart_items = page.locator("div.media-body h4 a")

    def add_to_cart(self, product_name):
        self.product_cards.filter(has_text=product_name).get_by_role("button", name="Add ").click()

    def checkout(self):
        self.checkout_link.click()
