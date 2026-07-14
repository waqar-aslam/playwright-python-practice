#from pages import orderhistorypage
from pages.orderhistorypage import orderhistorypage  # This imports the class

# page.wait_for_load_state("networkidle")
# page.wait_for_timeout(2000)  # Give time for dashboard to fully load
#print(user_credentials["username"])
#print(user_credentials["password"])


# Step 2: Navigate to orders page
# print("\n=== Navigating to Orders Page ===")
# page.get_by_role("button", name="ORDERS").click()
# dashboard = dashboardpage(page) this object creation is moved to loginpage class
# dashboard.ordernavlink(page) this method call is also moved to loginpage class

class dashboardpage:
        def __init__(self, page):
            self.page = page

        def navigate(self):
            self.page.get_by_role("button", name="ORDERS").click()
            order_page = orderhistorypage(self.page)
            return order_page