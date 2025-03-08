import pytest
from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """Setup and teardown for Selenium WebDriver"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver  # This allows the test to use the driver
    driver.quit()  # Teardown: close the browser after the test

@pytest.fixture(scope="function")
def login_page(driver):  # Injecting the driver into the login_page fixture
    """Fixture to return the LoginPage object"""
    return LoginPage(driver)
