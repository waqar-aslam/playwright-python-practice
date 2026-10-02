import re

from playwright.sync_api import Page


class CartPage:
    URL_PATTERN = re.compile(r".*/dashboard/cart")

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="My Cart")
        self.item_names = page.locator(".cartSection h3")
