import pytest
from playwright.sync_api import sync_playwright, Playwright, Page, expect
import re


def test_run(playwright:Playwright):
   # playwright.chromium.launch(headless=False)
    webkit = playwright.webkit
    browser = webkit.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://google.com")
    page.close()

def test_tryagain(playwright:Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://google.com")
    page.close()

def test_tryagain2(playwright:Playwright):
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://google.com")
    page.close()

def test_tryagain3(playwright:Playwright):
    browser = playwright.chromium.launch(headless=True,channel="msedge")
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://google.com")
    page.close()

def test_tryagain4(playwright:Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/");
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("Learning@830$3mK2")
    page.get_by_role("combobox").select_option("Teacher")
    page.get_by_role("checkbox",name="terms").check()
    page.get_by_role("button",name="Sign In").click()
    #expect(page).to_have_url("https://rahulshettyacademy.com/.*")
    expect(page).to_have_url(re.compile(".*shop"))

@pytest.mark.smoke
def test_addToCard(playwright:Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/");
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("Learning@830$3mK2")
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
def test_handleChildWindow(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/");
    with page.expect_popup() as popup:
        page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material").click()
        childWindow = popup.value
        redtext = childWindow.locator(".red").text_content()
        emailtextsplited = redtext.split(" at ")
        emailtextsecondsplit = emailtextsplited[1].split(" ")
        emailtext = emailtextsecondsplit[0].strip()
        assert(emailtext == "mentor@rahulshettyacademy.com")

#Handling child windows in Playwright
def test_handleChildWindow2(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    with page.expect_popup() as popup:
        page.get_by_role("link", name="Free Access to InterviewQues/ResumeAssistance/Material").click()
        childWindow = popup.value
        expect(childWindow).to_have_url("https://rahulshettyacademy.com/documents-request")
        expect(childWindow.get_by_text("contact@rahulshettyacademy.com")).to_have_text("contact@rahulshettyacademy.com")