import json
import re

from playwright.sync_api import Page, Response

from pages.cart_page import CartPage
from pages.order_history_page import OrderHistoryPage
from pages.product_details_page import ProductDetailsPage

PRODUCTS_API = "/api/ecom/product/get-all-products"
ADD_TO_CART_API = "**/api/ecom/user/add-to-cart"


class DashboardPage:
    """Product dashboard of the client app: navbar, filter sidebar and product cards."""

    URL_PATTERN = re.compile(r".*/dashboard/dash")

    def __init__(self, page: Page):
        self.page = page
        nav = page.locator("nav")
        self.logo_title = nav.locator(".logo h3")
        self.home_button = nav.get_by_role("button", name="HOME")
        self.orders_button = nav.get_by_role("button", name="ORDERS")
        self.cart_button = nav.get_by_role("button", name="Cart")
        self.sign_out_button = nav.get_by_role("button", name="Sign Out")

        self.sidebar = page.locator("#sidebar")
        self.search_input = self.sidebar.get_by_placeholder("search")
        self.min_price_input = self.sidebar.get_by_placeholder("Min Price")
        self.max_price_input = self.sidebar.get_by_placeholder("Max Price")

        self.product_cards = page.locator(".card-body")
        # textContent of <b> is the stored name; CSS uppercases it on screen
        self.product_names = self.product_cards.locator("h5 b")
        self.toast = page.locator("#toast-container")

    # ---------- navigation ----------
    def go_home(self):
        self.home_button.click()
        return self

    def go_to_orders(self):
        self.orders_button.click()
        return OrderHistoryPage(self.page)

    def go_to_cart(self):
        self.cart_button.click()
        return CartPage(self.page)

    def sign_out(self):
        from pages.login_page import LoginPage  # login_page imports this module

        self.sign_out_button.click()
        return LoginPage(self.page)

    # ---------- filters: each returns the product-list response it triggered ----------
    def _reload_products(self, action, **expected_filters) -> Response:
        """Run the action and return the product-list response whose request carries these filters."""

        def matches(response):
            if PRODUCTS_API not in response.url:
                return False
            sent = json.loads(response.request.post_data or "{}")
            return all(sent.get(key) == value for key, value in expected_filters.items())

        with self.page.expect_response(matches) as response:
            action()
        return response.value

    def search(self, text):
        self.search_input.fill(text)
        return self._reload_products(lambda: self.search_input.press("Enter"), productName=text)

    def filter_by_price(self, min_price=None, max_price=None):
        """Apply one or both price bounds and return the response for the final request.

        The site sends a request on Enter, and another when a changed price field loses focus.
        When both bounds are set, wait for the blur request before pressing Enter, so a slow
        earlier response can't arrive last and overwrite the filtered list.
        """
        if min_price is not None and max_price is not None:
            self.min_price_input.fill(str(min_price))
            self._reload_products(lambda: self.max_price_input.fill(str(max_price)), minPrice=min_price)
            field = self.max_price_input
        else:
            field = self.min_price_input if min_price is not None else self.max_price_input
            field.fill(str(min_price if min_price is not None else max_price))
        return self._reload_products(lambda: field.press("Enter"), minPrice=min_price, maxPrice=max_price)

    def filter_checkbox(self, label):
        """Checkbox in the sidebar by its exact label ("shirts" doesn't match "t-shirts")."""
        return (
            self.sidebar.locator(".form-group")
            .filter(has=self.page.get_by_text(label, exact=True))
            .locator("input[type=checkbox]")
        )

    def set_filter(self, label, checked=True):
        checkbox = self.filter_checkbox(label)
        return self._reload_products(lambda: checkbox.set_checked(checked))

    # ---------- product cards ----------
    def product_card(self, name):
        return self.product_cards.filter(has=self.page.get_by_text(name, exact=True))

    def view_product(self, name):
        self.product_card(name).get_by_role("button", name="View").click()
        return ProductDetailsPage(self.page)

    def add_to_cart(self, name) -> Response:
        with self.page.expect_response(ADD_TO_CART_API) as response:
            self.product_card(name).get_by_role("button", name="Add To Cart").click()
        return response.value
