from playwright.sync_api import Page, expect

from pages.automation_practice_page import AutomationPracticePage

# Use of locator Get By Placeholder
def test_demoPlaceHolder(page : Page):
    practice_page = AutomationPracticePage(page).open()
    expect(practice_page.hide_show_input).to_be_visible()
    #page.locator("#hide-textbox").click()
    practice_page.hide_button.click()
    expect(practice_page.hide_show_input).to_be_hidden()
    page.close()

# Handling alerts
def test_demoHandleAlert(page : Page):

    page.on("dialog", lambda dialog: dialog.accept())
    practice_page = AutomationPracticePage(page).open()
    #page.wait_for_selector("#confirmbtn")
    #print(page.locator("#confirmbtn").count())
    practice_page.confirm_button.click()
    #sleep(4)
    #page.locator("#confirmbtn").click()
    #page.close()

#Handling frames
def test_demoHandleFrames(page : Page):
    pageframe = AutomationPracticePage(page).open().courses_frame
    pageframe.get_by_role("link",name="All Access plan").click()
    expect(pageframe.locator("body")).to_contain_text("Subscibers")