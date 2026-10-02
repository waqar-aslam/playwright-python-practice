import re

from playwright.sync_api import Page, expect

from pages.automation_practice_page import AutomationPracticePage
from pages.practice_login_page import PracticeLoginPage
from pages.shop_page import ShopPage
from Utils.data_reader import get_users


def test_run(page: Page):
    PracticeLoginPage(page).open()
    # page.close()


def test_tryagain(page: Page):
    PracticeLoginPage(page).open()
    # page.close()


def test_tryagain2(page: Page):
    PracticeLoginPage(page).open()
    # page.close()


def test_tryagain3(page: Page):
    PracticeLoginPage(page).open()
    # page.close()


def test_tryagain4(page: Page):
    login_page = PracticeLoginPage(page).open()
    user = get_users()[2]
    login_page.login(user["username"], user["password"], accept_terms=True)
    expect(page).to_have_url(ShopPage.URL_PATTERN)


def test_addToCard(page: Page):
    login_page = PracticeLoginPage(page).open()
    user = get_users()[2]
    shop = login_page.login(user["username"], user["password"])
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
    childWindow = popup.value
    expect(childWindow.locator(".red")).to_contain_text("mentor@rahulshettyacademy.com")
    redtext = childWindow.locator(".red").text_content()
    emailtextsplited = redtext.split(" at ")
    emailtextsecondsplit = emailtextsplited[1].split(" ")
    emailtext = emailtextsecondsplit[0].strip()
    assert (emailtext == "mentor@rahulshettyacademy.com")


# Handling child windows in Playwright
def test_handleChildWindow2(page: Page):
    login_page = PracticeLoginPage(page).open()
    with page.expect_popup() as popup:
        login_page.free_access_link.click()
    childWindow = popup.value
    expect(childWindow).to_have_url(re.compile(r".*/documents-request"))
    expect(childWindow.get_by_text("contact@rahulshettyacademy.com")).to_have_text("contact@rahulshettyacademy.com")


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
