from playwright.sync_api import Page, expect

from pages.automation_practice_page import AutomationPracticePage


# Use of locator Get By Placeholder
def test_demoPlaceHolder(page: Page):
    practice_page = AutomationPracticePage(page).open()
    expect(practice_page.hide_show_input).to_be_visible()
    practice_page.hide_button.click()
    expect(practice_page.hide_show_input).to_be_hidden()


# Handling frames
def test_demoHandleFrames(page: Page):
    pageframe = AutomationPracticePage(page).open().courses_frame
    pageframe.get_by_role("link", name="All Access plan").click()
    expect(pageframe.locator("body")).to_contain_text("Subscibers")
