"""The BasePage class contains common Selenium actions."""
import json
import logging
import os
import time
from datetime import datetime

import pandas as pd
import pyautogui
import pytz
from bs4 import BeautifulSoup
from selenium.common import ElementNotVisibleException, StaleElementReferenceException, TimeoutException, \
    NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.window_dialog import window as WD

from config.config import TestData
from utils.db_connection import DatabaseHelper
from utils.enums import WaitType


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, WaitType.WEB_DRIVER_WAIT.value)
        self._short_wait = WebDriverWait(self.driver, WaitType.SHORT.value)
        self._long_wait = WebDriverWait(self.driver, WaitType.LONG.value)
        self._fluent_wait = WebDriverWait(self.driver, WaitType.FLUENT.value, poll_frequency=1,
                                          ignored_exceptions=[ElementNotVisibleException])
        self.db = DatabaseHelper(TestData.HOST, TestData.USER_NAME, TestData.PASSWORD, TestData.DB_NAME, TestData.PORT)
        self.word_doc = None
        self.download_dir = None

    def open_url(self, url):
        self.driver.get(url)
        logging.info(f"Navigating to {self.get_title()} application")
        time.sleep(5)

    def get_element(self, locator):
        return self.driver.find_element(locator)

    def get_web_element(self, by, value):
        return self._wait.until(EC.presence_of_element_located((by, value)))

    def get_all_element(self, locator):
        elements = self._wait.until(EC.presence_of_element_located(locator))
        return elements

    def get_element_with_retry(self, locator, max_retries=3):
        for attempt in range(max_retries):
            try:
                return self.driver.find_element(*locator)
            except StaleElementReferenceException:
                print(f"Retrying... Attempt {attempt + 1} of {max_retries}")
        raise Exception("Element not found after multiple attempt")

    def click_element(self, locator):
        element = self.get_element(locator)
        self.highlight_element(element, "green")
        element.click()

    def click(self, locator):
        el = self._wait.until(EC.element_to_be_clickable(locator))
        el.click()

    def click_web_element(self, locator):
        element = self.driver.find_element(*locator)  # Unpack the locator tuple and find the element
        element.click()  # Now click the element

    def js_click(self, locator):
        self.driver.execute_script("arguments[0].click();", locator)

    def js_click_element(self, locator_type, locator_value):
        """Reusable method to click an element using JavaScript."""
        element = self._wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
        self.driver.execute_script("arguments[0].click();", element)

    def close_browser(self):
        self.driver.quit()

    def enter_text(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def send_text(self, element_locator, text):
        element = self._wait.until(EC.presence_of_element_located(element_locator))
        element.clear()
        element.send_keys(text)

    def send_text_enter(self, locator, text):
        search_box = self._wait.until(EC.element_to_be_clickable(locator))
        search_box.send_keys(text + Keys.ENTER)

    def get_element_text(self, locator):
        element = self._wait.until(EC.visibility_of_element_located(locator))
        self.highlight_element(element, "green")
        return element.text

    def get_title(self):
        return self.driver.title

    def get_all_text_from_elements(self, locator):
        elements = self._wait.until(EC.presence_of_all_elements_located(locator))
        return [element.text for element in elements]

    @staticmethod
    def get_tooltip_text(self, element):
        tooltip_text = element.get_attribute("title")
        return tooltip_text if tooltip_text else element.get_attribute("aria-label")

    def clear_text(self, locator):
        el = self._wait.until(EC.element_to_be_clickable(locator))
        el.clear()

    def find_element_above(self, ref_element, tag="input"):
        """Uses Selenium 4 Relative Locators"""
        return self.driver.find_element(locate_with(By.TAG_NAME, tag).above(ref_element))

    def open_new_tab(self):
        """Uses Selenium 4 to open a new tab"""
        self.driver.switch_to.new_window('tab')

    def get_attribute_value(self, locator, value):
        ele = self._wait.until(EC.visibility_of_element_located(locator))
        return ele.get_attribute(value)

    def take_screenshot(self, filename="screenshot.png"):
        """Uses Selenium 4 full-page screenshot capability"""
        self.driver.save_screenshot(filename)

    def is_element_displayed(self, element_locator):
        try:
            return self._wait.until(EC.visibility_of_element_located(element_locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, element_locator):
        try:
            self._wait.until(EC.presence_of_element_located(element_locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, element_locator):
        try:
            return self._wait.until(EC.visibility_of_element_located(element_locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_clickable(self, element_locator):
        try:
            return self._wait.until(EC.element_to_be_clickable(element_locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def handle_alert(self, accept=True):
        alert = self._wait.until(EC.alert_is_present())

        if accept:
            alert.accept()
        else:
            alert.dismiss()

    def wait_for_element(self, locator):
        self._wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility_of_element(self, locator):
        self._wait.until(EC.visibility_of_element_located(locator))

    def wait_for_invisibility_of_element(self, locator):
        self._wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text_in_element(self, locator, text):
        self._wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_page_load(self):
        self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    def js_wait_for_page_load(self):
        while True:
            if self.driver.execute_script("return document.readState") == "complete":
                break

    """
    The lambda driver is part of the expected conditions (EC) logic in WebDriverWait.

        The until() method expects a callable (a function) that takes the driver as an argument.
        The lambda driver creates an anonymous function (a function without a name) that:
        ✅ Accepts the driver instance
        ✅ Executes the JavaScript code to check document.readyState
        ✅ Returns True when the condition is met
        The lambda function is repeatedly called every poll_frequency seconds until the condition is met or the timeout
    """

    def js_wait_for_page(self, time_unit_seconds):
        WebDriverWait(self.driver, time_unit_seconds).until(
            lambda driver: self.driver.execute_script("return document.readyState") == "complete"
        )

    def fluent_wait(self, locator):
        try:
            return self._fluent_wait.until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            print("Element was not found within the timeout period")

    def longWait_for_element(self, locator):
        try:
            return self._long_wait.until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {WaitType.WEB_DRIVER_WAIT.value} seconds")

    def select_option(self, locator, select_by, option):
        if isinstance(locator, tuple) and locator[0].lower() == "xpath":
            dropdown_element = self._wait.until(
                EC.presence_of_element_located(locator))
        else:
            dropdown_element = locator
        time.sleep(0.6)
        select = Select(dropdown_element)
        if select_by == 'text':
            select.select_by_visible_text(option)
        elif select_by == 'value':
            select.select_by_value(option)
        elif select_by == 'index':
            select.select_by_index(option)
        else:
            raise ValueError("Invalid 'select_by' option. Use 'text', 'value', or 'index'.")

    @staticmethod
    def get_selected_user_email(locator):
        dropdown = Select(locator)
        selected_option = dropdown.first_selected_option
        selected_value = selected_option.get_attribute('value')
        return selected_value

    def select_text_from_dropdown(self, dropdown_button, dropdown_val):
        self.click(dropdown_button)
        self.click(dropdown_val)

    def js_select_dropdown_option(self, dropdown_locator, dropdown_val):
        self.js_click_element(*dropdown_locator)
        self.js_click_element(*dropdown_val)

    def get_all_selected_options(self, locator_type, locator):
        """locator_type (str): The type of locator (e.g., "id", "name", "xpath").
        locator (str): the locator value """
        element = self._wait.until(
            EC.presence_of_element_located((locator_type, locator))
        )
        dropdown = Select(element)
        selected_options = dropdown.all_selected_options
        return [option.text for option in selected_options]

    @staticmethod
    def get_text_from_drop_down(locator):
        dropdown = Select(locator)
        return dropdown.first_selected_option.text

    def double_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.double_click(element).perform()

    def context_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.context_click(element).perform()

    def hover_and_get_text(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).perform()
        return element.text

    def scroll_to_element(self, locator):
        self.driver.execute_script("argument[0].scrollIntoView(true);", self.get_element(locator))

    def count_elements(self, locator):
        elements = self._wait.until(EC.presence_of_all_elements_located(locator))
        return len(elements)

    def get_page_max_number(self, locator):
        """Get the max number from the web-table pagination"""
        html = self.get_element(locator).get_attribute("outerHtml")
        soup = BeautifulSoup(html, 'lxml')
        max_number = soup.select_one('div.pagination > span').text.split(' ')[-1]  # Store result
        return int(max_number)

    def get_text_page_source(self, expected_text):
        page_source = self.driver.page_source
        if expected_text in page_source:
            print(f"Text '{expected_text}' found in the page source")
        else:
            print(f"Text '{expected_text}' not found in the page source")

    def get_text_from_source(self, locator):
        """
        get the page source of the current page
        :param locator:
        :return:
        """
        return self.driver.execute_script(f"return arguments[0].outerHTML;", locator)

    def js_get_page_source_usingJs(self):
        return self.driver.execute_script("return document.documentElement.outerHTML")

    def js_get_page_source_using(self, locator):
        return self.driver.execute_script("return document.documentElement.outerHTML")

    def get_page_source_usingJs(self, loc_type, locator):
        """
        driver.execute_script("return document.getElementsByTagName('html)[0].innerHtml")
        :param loc_type:
        :param locator:
        :return:
        eg: self.get_page_source_usingJs("ByClassName", "<class-name>"))
        """
        content = self.driver.execute_script(f"return document.getElements{loc_type}({locator}')[0].innerHTML")
        soup = BeautifulSoup(content, 'lxml')
        return soup.prettify()

    def perform_actions(self, actions_list):
        """
        Perform a sequence of actions using ActionChains.

        Example:
        actions_list = [
            {'action': 'move_to_element', 'by': By.ID, 'value': 'exampleElement1'},
            {'action': 'click', 'by': By.XPATH, 'value': "//button[@id='exampleButton']"},
            {'action': 'double_click', 'by': By.CLASS_NAME, 'value': 'exampleClass'},
            # Add more actions as needed
        ]
        :param actions_list: List of action dictionaries.
        :return: None
        """
        action_chains = ActionChains(self.driver)

        for action in actions_list:
            element = self.get_web_element(action['by'], action['value'])

            match action['action']:  # Python 3.10+ feature
                case 'move_to_element':
                    action_chains.move_to_element(element)
                case 'click':
                    action_chains.click(element)
                case 'double_click':
                    action_chains.double_click(element)
                case 'context_click':
                    action_chains.context_click(element)
                case _:
                    raise ValueError(f"Unsupported action: {action['action']}")

        if action_chains:
            action_chains.perform()

    def drag_and_drop(self, source_locator, target_locator):
        source_element = self.get_element(source_locator)
        target_element = self.get_element(target_locator)

        action_chains = ActionChains(self.driver)
        action_chains.drag_and_drop(source_element, target_element).perform()

    @staticmethod
    def click_element_with_robot(element):
        location = element.location_once_scrolled_into_view
        pyautogui.click(location['x'], location['y'])

    def perform_robot_actions(self, actions_list):
        """
        Perform a sequence of robot actions.

        Example:
        actions_list = [
            {'action': 'click', 'by': By.ID, 'value': 'exampleButton'},
            {'action': 'type', 'by': By.NAME, 'value': 'exampleInput', 'text': 'Hello, World!'},
            {'action': 'scroll', 'direction': 'down', 'amount': 3},
        ]
        :param actions_list: List of action dictionaries.
        :return: None
        """
        for action in actions_list:
            if action['action'] == 'click':
                element = self.get_web_element(action['by'], action['value'])
                self.click_element_with_robot(element)

            elif action['action'] == 'type':
                if 'text' not in action:
                    raise ValueError(f"Missing 'text' parameter in action: {action}")
                element = self.get_web_element(action['by'], action['value'])
                self.type_with_robot(element, action['text'])

            elif action['action'] == 'scroll':
                if 'direction' not in action or 'amount' not in action:
                    raise ValueError(f"Missing 'direction' or 'amount' parameter in action: {action}")
                self.scroll_with_robot(action['direction'], action['amount'])

            else:
                raise ValueError(f"Unsupported action: {action['action']}")

            # Add more actions as needed

    # pyautogui: This is the Python library for GUI automation, which includes functions for simulating mouse and
    # keyboard actions. pip install pyautogui

    @staticmethod
    def type_with_robot(element, text):
        element.click()
        pyautogui.typewrite(text)

    @staticmethod
    def scroll_with_robot(direction, amount):
        if direction == 'up':
            pyautogui.scroll(amount)
        elif direction == 'down':
            pyautogui.scroll(-amount)

    def highlight_element(self, element, color):
        original_style = element.get_attribute("style")
        new_style = "background-color:yellow;border: 1px solid " + color + original_style
        self.driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", element)
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)

    def get_page_source(self):
        return self.driver.page_source

    def assert_true(self, locator):
        ele = self.is_element_present(locator)
        assert ele == True, f"Expected True, but got {ele})"

    def assert_element_locator(self, locator, expected_text):
        element = self.get_element(locator)
        actual_text = element.text
        assert expected_text in actual_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'."

    @staticmethod
    def assert_element_text(actual_text, expected_text):
        assert expected_text in actual_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'."

    def assert_element_present(self, locator):
        try:
            self._wait.until(EC.presence_of_element_located(locator))
            assert True, f"Element located by {locator} is present."
        except Exception as e:
            assert False, f"Element located by {locator} is not present. {str(e)}"

    @staticmethod
    def assert_any_of_text(actual_text, expected_text):
        assert (actual_text in expected_text, f"Actual value should be one of {expected_text}")

    def assert_text_page_source(self, expected_text, locator):
        assert expected_text in self.js_get_page_source_using(
            locator), f"Expected text '{expected_text}' not found in the page source"

    def validate_grid(self, grid_locator, expected_data):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        actual_data = [cell.text for cell in grid.find_elements(By.TAG_NAME, 'td')]

        assert actual_data == expected_data, f"Grid validation failed. Expected: {expected_data}, Actual: {actual_data}"

    def iterate_grid_rows(self, grid_locator):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            # Process each cell in the row
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                print(cell.text)

    def iterate_grid(self, grid_locator):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')

            for cell in cells:
                print(f"Row: {rows.index(row) + 1}, Column: {cells.index(cell) + 1}, Text: {cell.text}")

    def validate_grid_data(self, grid_locator, expected_data):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row_index, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, 'td')

            for col_index, cell in enumerate(cells):
                actual_data = cell.text
                expected_value = expected_data[row_index][col_index]

                assert actual_data == expected_value, f"Grid validation failed at Row {row_index + 1}, Column {col_index + 1}. Expected: {expected_value}, Actual: {actual_data}"

    def upload_file(self, file_input_locator, file_path):
        file_input = self._wait.until(EC.presence_of_element_located(file_input_locator))
        file_input.send_keys(file_path)

    def get_network_performance(self):
        performance_logs = self.driver.get_log('performance')

        # Read network logs
        network_logs = [json.loads(log['message'])['message'] for log in performance_logs if
                        'Network' in log['message']]

        # Extract network information
        network_info = [entry['params'] for entry in network_logs if 'params' in entry]

        # Extract status codes from network information
        status_codes = [entry['response']['status'] for entry in network_info if 'response' in entry]

        return status_codes

    def read_csv_from_downloads(self, file_name, locator, button):

        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            download_dir = os.path.join(user_profile, 'Downloads')
        else:
            print("Failed to retrieve user profile directory")
            return None
        # Construct the full path to the CSV file
        file_path = os.path.join(download_dir, file_name)

        if os.path.exists(file_path):
            print(f"The '{file_name}' already exists in the Downloads directory. Removing it. ")
            os.remove(file_path)

        print("Downloading CSV file...")
        # define the method in base page and call it here
        self.csv_download_file(locator, button)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print("Error: ", e)
        else:
            print(f"File '{file_name}' not found in Downloads directory.")
            return None

    def get_word_file_document_file_path(self, file_name, download_button):
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            download_dir = os.path.join(user_profile, 'Downloads')
        else:
            print("Failed to retrieve user profile directory")
            return None
        # Construct the full path to the CSV file
        file_path = os.path.join(download_dir, file_name)

        if os.path.exists(file_path):
            print(f"The '{file_name}' already exists in the Downloads directory. Removing it. ")
            os.remove(file_path)

        print("Downloading word file...")
        # define the method in base page and call it here
        self.click(download_button)
        time.sleep(6)
        WD.save_download_file(file_name, file_path)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print("Error: ", e)
        else:
            print(f"File '{file_name}' not found in Downloads directory.")
            return None

    def csv_download_file(self, locator, button):
        self.clear_text(locator)
        self.send_text(locator, "URL")
        self.click_element(button)
        time.sleep(5)
        pyautogui.hotkey('enter')
        time.sleep(5)

    def connect_database(self, query):
        return self.db.execute_query(query)

    def get_all_rows_columns(self, query):
        logging.info("Validating records from database")
        return self.db.fetch_rows_with_column_names(query)

    def get_column_value(row, column_name):
        """
        Get the value of a column from a row dictionary.

        Args:
            row (dict): Dictionary representing a row with column names as keys.
            column_name (str): Name of the column whose value is to be retrieved.

        Returns:
            value: Value of the specified column, or None if the column doesn't exist.
        """
        return row.get(column_name)

    # Example dictionary representing a row
    # row = {'column1': 'value1', 'column2': 'value2', 'column3': 'value3'}
    #
    # # Iterate over the keys (column names)
    # for column_name in row.keys():
    #     print(column_name)
    #
    # # Iterate over the items (column name and value)
    # for column_name, value in row.items():
    #     print(column_name, value)

    def del_records_from_table(self, query):
        logging.info("Deleting records from the table")
        self.db.delete_query(query)

    @staticmethod
    def current_date(formate, time_type):
        """
        Fixture to get the current date in the desired format.
        """
        # Customize the desired format here
        if formate == "-":
            date_format = "%Y-%m-%d"
        elif formate == "/":
            date_format = "%m/%d/%Y"
        elif formate == "Ymd":
            date_format = "%Y-%m-%d"
        else:
            date_format = "%m%d%Y"
        local_time = datetime.now()
        if time_type == "GMT":
            get_timezone = pytz.timezone(time_type)
            get_time = local_time.astimezone(get_timezone)
            current_date = get_time.strftime(date_format)
        else:
            current_date = datetime.now().strftime(date_format)
        return current_date

    @staticmethod
    def read_immediate_next_string(list_of_string):
        immediate_next_string = []
        for string in list_of_string:
            # split the current string by spaces
            words = string.split()
            # if there's at least one more word after the current one, add it to the result
            if len(words) > 1:
                immediate_next_string.append([1])
            else:
                immediate_next_string.append([None])  # if no word found after, add none
        return immediate_next_string

    @staticmethod
    def upload_file_window(file_path):
        pyautogui.write(file_path)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.press('enter')

    def upload_file(self, locator_type, locator, file_path):
        element = self._wait.until(
            EC.presence_of_element_located((locator_type, locator))
        )
        element.send_keys(file_path)
