from pages.base_page import BasePage
from selenium.webdriver.common.by import By


# from locators.login_locators import USERNAME_FIELD, PASSWORD_FIELD, LOGIN_BUTTON


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "Logon")

    def __init__(self, driver, url, user_name, password):
        super().__init__(driver)
        self.login_url = url
        self.user_name = user_name
        self.password = password

    def navigate_application(self):
        self.driver.get(self.login_url)  # Navigate to the login URL

    def login(self):
        self.enter_text(self.USERNAME_FIELD, self.user_name)
        self.enter_text(self.PASSWORD_FIELD, self.password)
        self.click(self.LOGIN_BUTTON)

    def login_with_new_tab(self):
        self.user_name = "Testing"
        """Example using Selenium 4 new tab feature"""
        self.enter_text(self.USERNAME_FIELD, self.user_name)
        self.enter_text(self.PASSWORD_FIELD, self.password)
        self.click(self.LOGIN_BUTTON)
