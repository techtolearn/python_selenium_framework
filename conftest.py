import os
import time
from datetime import datetime
from pathlib import Path

import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

from config.config import TestData
from pages.login_page import LoginPage
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERID")
URL = TestData.BASE_URL


def pytest_addoption(parser):
    """ This function adds an argument to choose the browser """
    parser.addoption("--browser_name", action="store", default="chrome")


@pytest.fixture(scope="class")
def driver(request):  # Added 'request' parameter for fixture
    """ Here we are doing setup for browser and the URL """

    global driver
    browser_name = request.config.getoption("browser_name")
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": TestData.DOWNLOAD_FOLDER,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "log": capabilities['goog:loggingPrefs']
        })
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument('--disable-gpu')
        if TestData.HEADLESS:
            chrome_options.add_argument('--headless')

        services = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=services, options=chrome_options)

    elif browser_name == "firefox":
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    elif browser_name == "IE":
        service = Service(IEDriverManager().install())
        driver = webdriver.Ie(service=service)
    # tear down
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    time.sleep(1)
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):  # Injecting the driver into the login_page fixture
    """Fixture to return the LoginPage object"""
    return LoginPage(driver, URL, USERNAME, PASSWORD)  # Pass LOGIN_URL to LoginPage


reports_dir = ''


def create_report_folder():
    """ Creates a report folder with the datetime stamp """
    global reports_dir
    # if config is set to create individual report then create individual report with timestamp else create single
    # report
    if TestData.INDIVIDUAL_REPORT:
        reports_dir = Path(TestData.REPORT_FOLDER, datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        reports_dir.mkdir(parents=True, exist_ok=True)
    else:
        reports_dir = Path(TestData.REPORT_FOLDER)
        if not os.path.exists(reports_dir):
            reports_dir.mkdir(parents=True, exist_ok=False)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ Updates the default configurations of pytest """
    # Create the project folder
    create_report_folder()
    # custom report file
    report = reports_dir / "report.html"
    # adjust plugin options (Updating the report path)
    config.option.htmlpath = report
    config.option.self_contained_html = True


def pytest_html_report_title(report):
    """ Sets a custom title for the HTML report (browser tab) """
    report.title = "API Test Automation Results"


def pytest_html_results_summary(prefix, summary, postfix):
    """ Adds user-defined text at the top of the HTML report """
    user_defined_text = html.p("Custom Report: This execution is for testing API automation results.")
    prefix.extend([user_defined_text])


def pytest_html_results_table_header(cells):
    """ Adds two columns (Description and time) to the report table """
    cells.insert(2, html.th('Description'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """ Adds row two column values to the row """
    cells.insert(2, html.td("report.description"))
    cells.insert(3, html.td(datetime.now(), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    """ Saves the captured screenshot to the report directory """
    global reports_dir
    reports_dir = str(Path(reports_dir))
    if not os.path.exists(os.path.join(reports_dir + '/tests')):
        os.makedirs(reports_dir + '/tests')

    # save the Screenshot
    try:
        # Save the screenshot to the file
        driver.get_screenshot_as_file(reports_dir + '/' + name)
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
