from playwright.sync_api import Page, expect

# Test scenario: in the offers web table, the price of Rice should be 37.
# The price column is found by its header, so the test survives column reordering.


def test_demoWebTables(page: Page):
    page.goto("/seleniumPractise/#/offers")
    headers = page.locator("th")
    expect(headers.first).to_be_visible()
    header_texts = headers.all_inner_texts()
    price_col = next((i for i, text in enumerate(header_texts) if "Price" in text), None)
    assert price_col is not None, f"No Price column in headers {header_texts}"

    rice_row = page.locator("tr").filter(has_text="Rice")
    expect(rice_row.locator("td").nth(price_col)).to_have_text("37")
