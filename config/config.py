import os
from pathlib import Path


class TestData:
    BASE_URL = "https://www.creditkarma.com/auth/logon"
    API_BASE_URL = "https://reqres.in"

    # use os.path.join to create a path
    BASE_DIRECTORY = os.getcwd()
    ROOT_DIR = str(Path(__file__).resolve().parent.parent)
    ROOT_PATH = str(Path(__file__).parent.parent)
    INI_CONFIGS_PATH = os.path.join(ROOT_DIR, "ini_configs")
    DATA_FILES_PATH = os.path.join(ROOT_DIR, "data")

    DRIVER_PATH = os.path.join(BASE_DIRECTORY, 'drivers')
    DOWNLOAD_FOLDER = os.path.join(BASE_DIRECTORY, 'results', 'media', 'download')

    # Reporting

    REPORT_TITLE = "Test Automation Report"
    REPORT_FOLDER = os.path.join(BASE_DIRECTORY, '../results', 'reports')
    INDIVIDUAL_REPORT = False
    LOG_FOLDER = os.path.join(BASE_DIRECTORY, '../results', 'logs')

    # Excel
    AUTOMATION_USER_AGENET: str = ""
    DATA_PATH: Path = Path(Path(__file__).absolute().parent.parent, "data")
    CHROME_DOWNLOAD_DIRECTORY: Path = DATA_PATH / "downloads"
    DIFF_TOLERANCE_PERCENT: float = 0.01
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

    # DRIVER
    WEB_DRIVER_WAIT = 60
    HEADLESS = False
    ACTION_DELAY = 2
    DOWNLOAD_WAIT_TIME = 60

    # Error handling
    ALLURE_RESULTS_PATH = os.path.join(ROOT_DIR, "allure-results")

    # Application Test Data
    menu = ['', '']
    drop_down = ['', '']

    # DB Driver details
    HOST = "<host-url>"
    USER_NAME = "<usr-name>"
    PASSWORD = "<pwd>"
    PORT = 3422
    DB_NAME = "<database_name>"

    EMPLOYEE = """select name, city, phone, address, salary, company from employee where employee_ID= '"""
