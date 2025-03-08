from pages.base_page import BasePage
from selenium.webdriver.common.by import By
# from locators.login_locators import USERNAME_FIELD, PASSWORD_FIELD, LOGIN_BUTTON


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://example.com/login")

    def login(self, username, password):
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def login_with_new_tab(self, username, password):
        """Example using Selenium 4 new tab feature"""
        self.open_new_tab()
        self.driver.get("https://example.com/login")
        self.login(username, password)
