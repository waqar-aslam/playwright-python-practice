import pytest
from playwright.sync_api import sync_playwright, Playwright, Page, expect
import re

from Utils.config_reader import settings, get_url
from Utils.data_reader import get_users
from tests.conftest import user_credentials


def test_run(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    #page.close()

def test_tryagain(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    #page.close()

def test_tryagain2(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    #page.close()

def test_tryagain3(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    #page.close()

def test_tryagain4(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    users = get_users()
    user = users[2]
    page.get_by_label("Username:").fill(user["username"])
    page.get_by_label("Password:").fill(user["password"])
    page.get_by_role("combobox").select_option("Teacher")
    page.get_by_role("checkbox",name="terms").check()
    page.get_by_role("button",name="Sign In").click()
    #expect(page).to_have_url("https://rahulshettyacademy.com/.*")
    expect(page).to_have_url(re.compile(".*shop"))

@pytest.mark.smoke
def test_addToCard(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    users = get_users()
    user = users[2]
    page.get_by_label("Username:").fill(user["username"])
    page.get_by_label("Password:").fill(user["password"])
    page.get_by_role("combobox").select_option("Teacher")
    page.get_by_role("button",name="Sign In").click()
    iphonelocator = page.locator("app-card").filter(has_text="iphone X")
    iphonelocator.get_by_role("button",name="Add ").click()
    nokiaEdgelocator = page.locator("app-card").filter(has_text="Nokia Edge")
    nokiaEdgelocator.get_by_role("button",name="Add ").click()
    page.get_by_text("Checkout ( 2 )").click()
    #page.get_by_role("link",name="Checkout ( 2 )").click()
    expect(page.locator("div.media-body h4 a")).to_have_count(2)
    #expect(page).to_have_url(re.compile(".*shop"))

@pytest.mark.regression#Handling child windows in Playwright
def test_handleChildWindow(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    with page.expect_popup() as popup:
        page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material").click()
        childWindow = popup.value
        redtext = childWindow.locator(".red").text_content()
        emailtextsplited = redtext.split(" at ")
        emailtextsecondsplit = emailtextsplited[1].split(" ")
        emailtext = emailtextsecondsplit[0].strip()
        assert(emailtext == "mentor@rahulshettyacademy.com")

#Handling child windows in Playwright
def test_handleChildWindow2(browser_instance):
    page = browser_instance
    page.goto(get_url("base_url"))
    with page.expect_popup() as popup:
        page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material").click()
        childWindow = popup.value
        expect(childWindow).to_have_url("https://rahulshettyacademy.com/documents-request")
        expect(childWindow.get_by_text("contact@rahulshettyacademy.com")).to_have_text("contact@rahulshettyacademy.com")