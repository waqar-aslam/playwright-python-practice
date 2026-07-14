from pages.orderdetailspage import orderdetailspage


# page.get_by_role("button", name="ORDERS").click()
# Step 3: Find the order in the table
# print(f"\n=== Searching for Order: {order_id} ===")
# row = page.locator("tr").filter(has_text=order_id)

# Step 4: Click View button
# row.get_by_role("button", name="View").click()


class orderhistorypage:
    def __init__(self,page):
        self.page = page



    def get_order(self,order_id):
        print(f"\n=== Searching for Order: {order_id} ===")
        row = self.page.locator("tr").filter(has_text=order_id)
        row.get_by_role("button", name="View").click()

        order_detail = orderdetailspage(self.page)
        return order_detail