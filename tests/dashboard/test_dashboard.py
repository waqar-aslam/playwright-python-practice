"""Dashboard of the client app: header, navigation, search, filters and product actions.

Expected results are computed from the API catalogue (`catalogue` fixture), so the tests keep
working when products change. Filter tests also check the request the UI sends, so a checkbox
that silently does nothing fails even when the visible list happens to match.
"""

import json
import re

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.dashboard_page import DashboardPage
from pages.order_history_page import OrderHistoryPage
from pages.product_details_page import ProductDetailsPage


def names(products):
    return [p["productName"] for p in products]


def expect_products(dashboard, expected):
    """The cards show exactly these product names, in catalogue order."""
    if expected:
        expect(dashboard.product_names).to_have_text(expected)
    else:
        expect(dashboard.product_cards).to_have_count(0)


def request_filters(response):
    return json.loads(response.request.post_data)


@pytest.mark.smoke
class TestDashboardHeader:
    def test_title_is_automation(self, dashboard):
        # The text is "Automation"; CSS uppercases it, so compare what the user sees
        expect(dashboard.logo_title).to_have_text("AUTOMATION", use_inner_text=True)

    def test_orders_link(self, dashboard, page):
        orders = dashboard.go_to_orders()
        expect(page).to_have_url(OrderHistoryPage.URL_PATTERN)
        expect(orders.heading).to_be_visible()

    def test_cart_link(self, dashboard, page):
        cart = dashboard.go_to_cart()
        expect(page).to_have_url(CartPage.URL_PATTERN)
        expect(cart.heading).to_be_visible()

    def test_home_link(self, dashboard, page):
        dashboard.go_to_orders()
        expect(page).to_have_url(OrderHistoryPage.URL_PATTERN)
        dashboard.go_home()
        expect(page).to_have_url(DashboardPage.URL_PATTERN)
        expect(dashboard.product_cards.first).to_be_visible()

    def test_sign_out_link(self, dashboard, page):
        login_page = dashboard.sign_out()
        expect(page).to_have_url(re.compile(r".*/auth/login"))
        expect(login_page.login_button).to_be_visible()


@pytest.mark.regression
class TestSearch:
    def test_search_by_full_name(self, dashboard, catalogue):
        for product in catalogue:
            response = dashboard.search(product["productName"])
            assert request_filters(response)["productName"] == product["productName"]
            expect_products(dashboard, [product["productName"]])

    def test_search_by_name_prefix(self, dashboard, catalogue):
        prefix = catalogue[0]["productName"].split()[0]
        dashboard.search(prefix)
        expect_products(dashboard, [n for n in names(catalogue) if n.startswith(prefix)])

    def test_search_with_no_match_shows_message(self, dashboard):
        dashboard.search("no-such-product-xyz")
        expect_products(dashboard, [])
        expect(dashboard.toast).to_contain_text("No Products Found")

    def test_clearing_search_restores_all_products(self, dashboard, catalogue):
        dashboard.search(catalogue[0]["productName"])
        expect_products(dashboard, [catalogue[0]["productName"]])
        dashboard.search("")
        expect_products(dashboard, names(catalogue))

    @pytest.mark.xfail(
        strict=True, reason="Site bug: search is case-sensitive, so the name as displayed (uppercased) finds nothing"
    )
    def test_search_by_name_as_displayed(self, dashboard, catalogue):
        lowercase = next((n for n in names(catalogue) if n != n.upper()), None)
        if lowercase is None:
            pytest.skip("Every product name is already uppercase")
        dashboard.search(lowercase.upper())
        expect_products(dashboard, [lowercase])


@pytest.mark.regression
class TestPriceFilter:
    @pytest.mark.parametrize(
        "min_price, max_price",
        [(0, 1_000_000), (11500, 11500), (20000, 60000), (60000, 70000)],
        ids=["all", "exact-price", "range", "no-match"],
    )
    def test_min_and_max_price(self, dashboard, catalogue, min_price, max_price):
        response = dashboard.filter_by_price(min_price, max_price)
        sent = request_filters(response)
        assert (sent["minPrice"], sent["maxPrice"]) == (min_price, max_price)
        expect_products(dashboard, [p["productName"] for p in catalogue if min_price <= p["productPrice"] <= max_price])

    @pytest.mark.xfail(strict=True, reason="Site bug: Min Price alone is ignored; it only applies with Max Price")
    def test_min_price_only(self, dashboard, catalogue):
        min_price = max(p["productPrice"] for p in catalogue)
        dashboard.filter_by_price(min_price=min_price)
        expect_products(dashboard, [p["productName"] for p in catalogue if p["productPrice"] >= min_price])

    @pytest.mark.xfail(strict=True, reason="Site bug: Max Price alone is ignored; it only applies with Min Price")
    def test_max_price_only(self, dashboard, catalogue):
        max_price = min(p["productPrice"] for p in catalogue)
        dashboard.filter_by_price(max_price=max_price)
        expect_products(dashboard, [p["productName"] for p in catalogue if p["productPrice"] <= max_price])


# (sidebar label, field it filters on: the same name in the request and in the catalogue)
CHECKBOX_FILTERS = [
    *[(label, "productCategory") for label in ("fashion", "electronics", "household")],
    *[(label, "productSubCategory") for label in ("t-shirts", "shirts", "shoes", "mobiles", "laptops")],
    *[(label, "productFor") for label in ("men", "women")],
]


@pytest.mark.regression
class TestCheckboxFilters:
    """Categories, Sub Categories and Search For: checking filters the list, unchecking restores it."""

    @pytest.mark.parametrize("label, field", CHECKBOX_FILTERS, ids=[f"{f}:{label}" for label, f in CHECKBOX_FILTERS])
    def test_checkbox_filters_products(self, dashboard, catalogue, label, field):
        response = dashboard.set_filter(label, checked=True)
        expect(dashboard.filter_checkbox(label)).to_be_checked()
        assert request_filters(response)[field] == [label]
        expect_products(dashboard, [p["productName"] for p in catalogue if p[field] == label])

        response = dashboard.set_filter(label, checked=False)
        expect(dashboard.filter_checkbox(label)).not_to_be_checked()
        assert request_filters(response)[field] == []
        expect_products(dashboard, names(catalogue))


@pytest.mark.regression
class TestProductActions:
    def test_view_button_on_each_product(self, dashboard, catalogue, page):
        for product in catalogue:
            details = dashboard.view_product(product["productName"])
            expect(page).to_have_url(ProductDetailsPage.URL_PATTERN)
            expect(page).to_have_url(re.compile(rf".*/product-details/{product['_id']}$"))
            expect(details.name).to_have_text(product["productName"])
            expect(details.price(product["productPrice"])).to_be_visible()
            dashboard = details.continue_shopping()
            expect(dashboard.product_cards.first).to_be_visible()

    def test_add_to_cart_button_on_each_product(self, dashboard, catalogue):
        # Checks the request and the toast, not the cart count: every login empties the shared
        # cart, so other tests logging in as the same user in parallel would make a count flaky.
        for product in catalogue:
            response = dashboard.add_to_cart(product["productName"])
            assert response.ok, f"Add to cart failed for {product['productName']}: HTTP {response.status}"
            assert json.loads(response.request.post_data)["product"]["_id"] == product["_id"]
            expect(dashboard.toast).to_contain_text("Product Added To Cart")
