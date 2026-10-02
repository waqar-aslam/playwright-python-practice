import re

from playwright.sync_api import Page, expect

from pages.automation_practice_page import AutomationPracticePage
from pages.practice_login_page import PracticeLoginPage
from pages.shop_page import ShopPage


def test_login_to_shop(page: Page):
    login_page = PracticeLoginPage(page).open()
    username, password = login_page.published_credentials()
    login_page.login(username, password, accept_terms=True)
    expect(page).to_have_url(ShopPage.URL_PATTERN)


def test_addToCard(page: Page):
    login_page = PracticeLoginPage(page).open()
    shop = login_page.login(*login_page.published_credentials())
    shop.add_to_cart("iphone X")
    shop.add_to_cart("Nokia Edge")
    shop.checkout()
    expect(shop.cart_items).to_have_count(2)


# Handling child windows in Playwright
def test_handleChildWindow(page: Page):
    login_page = PracticeLoginPage(page).open()
    # The popup is only available once the with-block exits
    with page.expect_popup() as popup:
        login_page.free_access_link.click()
    child_window = popup.value
    expect(child_window).to_have_url(re.compile(r".*/documents-request"))
    expect(child_window.locator(".red")).to_contain_text("mentor@rahulshettyacademy.com")

    # Pulling a value out of the child window's text
    red_text = child_window.locator(".red").text_content()
    email = red_text.split(" at ")[1].split(" ")[0].strip()
    assert email == "mentor@rahulshettyacademy.com"


def test_traverse_parent_to_child(page: Page):
    practice_page = AutomationPracticePage(page).open()
    parent = practice_page.switch_window_section
    expect(parent).to_be_visible()

    leftalign = parent.locator(".left-align")
    expect(leftalign).to_be_visible()

    fieldset = leftalign.locator("fieldset")
    expect(fieldset).to_be_visible()

    button = fieldset.locator("#openwindow")
    expect(button).to_have_text("Open Window")
    expect(button).to_be_visible()
    expect(button).to_be_enabled()
    button.click()
