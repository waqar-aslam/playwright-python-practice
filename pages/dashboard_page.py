import re

from playwright.sync_api import Page

from pages.order_history_page import OrderHistoryPage


class DashboardPage:
    URL_PATTERN = re.compile(r".*/dashboard/dash")

    def __init__(self, page: Page):
        self.page = page
        self.sidebar = page.locator("#sidebar")
        self.orders_button = page.get_by_role("button", name="ORDERS")

    def go_to_orders(self):
        self.orders_button.click()
        return OrderHistoryPage(self.page)
