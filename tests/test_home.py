from pages.home_page import HomePage
""" either follow test_loin.py where LoginPage has defined in conftest or follow below approach"""
def test_home_title(driver):
    home_page = HomePage(driver)
    # perform actions on home_page
    assert "Home" in driver.title