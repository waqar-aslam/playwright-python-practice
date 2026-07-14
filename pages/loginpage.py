from pages.dashboardpage import dashboardpage

# These commented code was initially written in test login class so now using Page Object Model
# This code is shifted in login page class
# page.goto("https://rahulshettyacademy.com/client/#/auth/login")
# page.get_by_placeholder(text="email@example.com").fill(user_credentials["username"])
# page.get_by_placeholder(text="enter your passsword").fill(user_credentials["password"])
# page.get_by_role("button",name="Login").click()
# Wait for login to complete and dashboard to load

class loginpage:
    def __init__(self, page):
        self.page = page

    def navigate(self, page):
        page.goto("https://rahulshettyacademy.com/client/#/auth/login")

    def login(self, page, username, password):
        page.get_by_placeholder(text="email@example.com").fill(username)
        page.get_by_placeholder(text="enter your passsword").fill(password)
        page.get_by_role("button", name="Login").click()

        # creating object of dashboard class
        dashboard = dashboardpage(self.page)
        return dashboard

