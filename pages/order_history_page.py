import logging
import re

from playwright.sync_api import Page

from pages.order_details_page import OrderDetailsPage

logger = logging.getLogger(__name__)


class OrderHistoryPage:
    URL_PATTERN = re.compile(r".*/dashboard/myorders")

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Your Orders")
        self.order_rows = page.locator("tr")

    def view_order(self, order_id):
        logger.info("Opening order %s", order_id)
        self.order_rows.filter(has_text=order_id).get_by_role("button", name="View").click()
        return OrderDetailsPage(self.page)
