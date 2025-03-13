import logging
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
def setup(request):  # Added 'request' parameter for fixture
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
def login_page(setup):  # Injecting the driver into the login_page fixture
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

    create_report_folder()

    # Log file configuration
    log_file = Path(reports_dir) / "logs" / "test_log.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure the 'logs' folder is created
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,  # Captures only errors and critical failures
        format="%(asctime)s [%(levelname)s] %(message)s - [%(filename)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    report = reports_dir / "report.html"
    config.option.htmlpath = report
    config.option.self_contained_html = True


def pytest_html_report_title(report):
    """ Sets a custom title for the HTML report (browser tab) """
    report.title = TestData.REPORT_TITLE


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
    cells.insert(2, html.td(report.description))
    cells.insert(3, html.td(datetime.now(), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == "call" and report.failed:
        logging.error(f"Test Failed: {item.name} - {call.excinfo}")
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                screenshot_html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                                  'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(screenshot_html))
        report.extra = extra


def _capture_screenshot(name):
    """Saves the captured screenshot to the report directory."""
    global reports_dir
    reports_dir = str(Path(reports_dir).resolve())

    if not os.path.exists(reports_dir + '/tests'):
        os.makedirs(reports_dir + '/tests')

    try:
        driver.get_screenshot_as_file(reports_dir + '/' + name)
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
