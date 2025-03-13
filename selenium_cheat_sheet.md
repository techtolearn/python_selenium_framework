# Selenium Python Automation Cheat Sheet

## Setup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##  Initialize Driver
driver = webdriver.Chrome()
driver.get("https://example.com")
driver.maximize_window()

## Locators

driver.find_element(By.ID, "element_id")
driver.find_element(By.NAME, "element_name")
driver.find_element(By.XPATH, "//div[@class='example']")
driver.find_element(By.CSS_SELECTOR, "div.example")
driver.find_element(By.CLASS_NAME, "example_class")
driver.find_element(By.TAG_NAME, "input")
driver.find_element(By.LINK_TEXT, "Click Me")
driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

## Relative Locators (Selenium 4)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.relative_locator import locate_with
driver.find_element(locate_with(By.TAG_NAME, "input").below({By.ID: "username"}))
driver.find_element(locate_with(By.TAG_NAME, "button").to_right_of({By.ID: "cancel_button"}))
driver.find_element(locate_with(By.TAG_NAME, "div").near({By.ID: "search_field"}))

## Waits

wait = WebDriverWait(driver, 10)

##  Explicit Wait
wait.until(EC.presence_of_element_located((By.ID, "element_id")))
wait.until(EC.element_to_be_clickable((By.ID, "element_id")))

## Actions

actions = ActionChains(driver)
element = driver.find_element(By.ID, "element_id")

###  Mouse Actions
actions.move_to_element(element).perform()
actions.context_click(element).perform()
actions.double_click(element).perform()
actions.click_and_hold(element).release().perform()

### Keyboard Actions
element.send_keys(Keys.RETURN)
element.send_keys(Keys.CONTROL, 'a')

## Handling Alerts

alert = driver.switch_to.alert
alert.accept()  # Accept alert
alert.dismiss()  # Dismiss alert
alert.send_keys("Text")  # Send text to alert

## Handling Frames

driver.switch_to.frame("frame_name")
driver.switch_to.default_content()  # Exit from frame

## Handling Windows

main_window = driver.current_window_handle
all_windows = driver.window_handles

for window in all_windows:
    if window != main_window:
        driver.switch_to.window(window)

## Handling Dropdowns

from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "dropdown_id"))
select.select_by_visible_text("Option 1")
select.select_by_value("value1")
select.select_by_index(1)

## Taking Screenshots

driver.save_screenshot("screenshot.png")

## Executing JavaScript

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

## Closing Browser

driver.quit()  # Close all windows
driver.close()  # Close current window

##  Best Practices

- Use Explicit Waits over Implicit Waits.
- Implement Page Object Model (POM) for maintainability.
- Use proper exception handling to improve test stability.
- Manage browser state to reduce flaky tests.
