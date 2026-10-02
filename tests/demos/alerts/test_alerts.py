from playwright.sync_api import Dialog, Page

from pages.automation_practice_page import AutomationPracticePage


def test_accept_alert(page: Page):
    practice_page = AutomationPracticePage(page).open()
    page.on("dialog", lambda dialog: dialog.accept())
    practice_page.alert_button.click()


def test_read_alert_message(page: Page):
    practice_page = AutomationPracticePage(page).open()
    messages = []

    def handle(dialog: Dialog):
        messages.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle)
    with page.expect_event("dialog"):
        practice_page.alert_button.click()
    assert "share this practice page" in messages[0]


def test_accept_confirm(page: Page):
    practice_page = AutomationPracticePage(page).open()
    page.on("dialog", lambda dialog: dialog.accept())
    practice_page.confirm_button.click()
