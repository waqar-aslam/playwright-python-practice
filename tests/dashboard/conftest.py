import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from Utils.data_reader import get_valid_user


@pytest.fixture(scope="session")
def catalogue(api_utils):
    """Unfiltered product list from the API: the source of truth for what each filter should show."""
    products = api_utils.get_products(get_valid_user())
    assert products, "Catalogue is empty; the dashboard tests need at least one product"
    return products


@pytest.fixture
def dashboard(page: Page) -> DashboardPage:
    """A logged-in dashboard with the product cards loaded."""
    user = get_valid_user()
    dashboard = LoginPage(page).open().login(user["username"], user["password"])
    expect(page).to_have_url(DashboardPage.URL_PATTERN)
    expect(dashboard.product_cards.first).to_be_visible()
    return dashboard
