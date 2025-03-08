"""The BasePage class contains common Selenium actions."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click_wait(self, locator):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(locator)).click()

    @staticmethod
    def click(self, locator):
        locator.click()

    def enter_text(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).text

    def find_element_above(self, ref_element, tag="input"):
        """Uses Selenium 4 Relative Locators"""
        return self.driver.find_element(locate_with(By.TAG_NAME, tag).above(ref_element))


    def open_new_tab(self):
        """Uses Selenium 4 to open a new tab"""
        self.driver.switch_to.new_window('tab')

    def take_screenshot(self, filename="screenshot.png"):
        """Uses Selenium 4 full-page screenshot capability"""
        self.driver.save_screenshot(filename)

