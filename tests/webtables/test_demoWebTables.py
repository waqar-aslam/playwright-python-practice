from playwright.sync_api import Page, expect


def test_demoWebTables(page:Page):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Price").count() > 0:
            price_col_value = index
            print(f" Price column value is : {price_col_value}")
            break
    riceRow = page.locator("tr").filter(has_text="Rice")
    expect(riceRow.locator("td").nth(price_col_value)).to_have_text("37")


   # for index in range(page.locator("tr").count()):
    #    if page.locator("tr").nth(index).filter(has_text="Rice").count() > 0:
     #       row_index = page.locator("tr").nth(index)
      #      break

 #   price_cell  = row_index.locator("td").nth(col_index)
 #   print("Column Index:", col_index)
  #  print("Selected Row:", row_index.inner_text())
  #  expect(price_cell).to_have_text("37")
