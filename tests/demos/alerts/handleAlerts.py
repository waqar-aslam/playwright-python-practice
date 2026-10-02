from playwright.sync_api import Page

from pages.automation_practice_page import AutomationPracticePage


def test_accept_alerts(page: Page):
    practice_page = AutomationPracticePage(page).open()
    page.on("dialog", lambda dialog: dialog.accept())
    practice_page.alert_button.click()
    page.close()


def test_print_dialog(page: Page):
    practice_page = AutomationPracticePage(page).open()

    page.on(
        "dialog",
        lambda dialog: (
            print(f"Alert message: {dialog.message}"),
            dialog.accept()
        )
    )

    practice_page.alert_button.click()
    page.close()

