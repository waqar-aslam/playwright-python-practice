from pages.OrderDetails import OrderDetails


class OrderHistory:
    def __init__(self, page):
        self.page = page


    def get_order(self, page,order_id):
        print(f"\n=== Searching for Order: {order_id} ===")
        row = self.page.locator("tr").filter(has_text=order_id)
        row.get_by_role("button", name="View").click()
        orderDetailsOBJ = OrderDetails(self.page,order_id)
        return orderDetailsOBJ