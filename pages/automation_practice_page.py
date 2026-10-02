from playwright.sync_api import Page


class AutomationPracticePage:
    """The /AutomationPractice/ page: alerts, frames, hide/show and window examples."""

    URL = "/AutomationPractice/"

    def __init__(self, page: Page):
        self.page = page
        self.hide_show_input = page.get_by_placeholder("Hide/Show Example")
        self.hide_button = page.get_by_role("button", name="Hide")
        self.alert_button = page.locator("#alertbtn")
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.courses_frame = page.frame_locator("#courses-iframe")
        self.switch_window_section = page.locator("div.block.large-row-spacer").filter(
            has=page.locator("legend", has_text="Switch Window Example")
        )

    def open(self):
        self.page.goto(self.URL)
        return self
