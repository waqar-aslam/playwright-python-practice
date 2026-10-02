from tkinter import dialog

from playwright.sync_api import Page


def test_accept_alerts(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("//input[@id='alertbtn']").click()
    page.close()


def test_print_dialog(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")

    page.on(
        "dialog",
        lambda dialog: (
            print(f"Alert message: {dialog.message}"),
            dialog.accept()
        )
    )

    page.locator("//input[@id='alertbtn']").click()
    page.close()

