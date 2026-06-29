from time import sleep

from playwright.sync_api import Page, expect

# Use of locator Get By Placeholder
def test_demoPlaceHolder(page : Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    #page.locator("#hide-textbox").click()
    page.get_by_role("button",name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()
    page.close()

# Handling alerts
def test_demoHandleAlert(page : Page):

    page.on("dialog", lambda dialog: dialog.accept())
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    #page.wait_for_selector("#confirmbtn")
    #print(page.locator("#confirmbtn").count())
    page.locator("#confirmbtn:visible").click()
    page.get_by_role("button",name="Confirm").click()
    #sleep(4)
    #page.locator("#confirmbtn").click()
    #page.close()

#Handling frames
def test_demoHandleFrames(page : Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    pageframe = page.frame_locator("#courses-iframe")
    pageframe.get_by_role("link",name="All Access plan").click()
    expect(pageframe.locator("body")).to_contain_text("Subscriber")