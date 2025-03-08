
def test_valid_login(login_page):  # login_page is automatically passed as a fixture
    login_page.login("user", "pass")
    assert "Dashboard" in login_page.driver.title


def test_invalid_login(login_page):
    login_page.login("wrong_user", "wrong_pass")
    assert "Invalid credentials" in login_page.driver.page_source
