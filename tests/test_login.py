import pytest
from selenium.webdriver.common.by import By


def test_valid_login(login_page):  # login_page is automatically passed as a fixture
    login_page.navigate_application()
    login_page.login()
    print()
    assert "Credit Karma" in login_page.driver.title


def test_invalid_login(login_page):
    login_page.navigate_application()
    login_page.login_with_new_tab()
    error_message = login_page.driver.find_element(By.ID, 'email-error')
    assert "Please enter a valid email address." in error_message.text
