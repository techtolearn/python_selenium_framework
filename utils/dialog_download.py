from pywinauto import Application
from pywinauto.timings import wait_until_passes
import time


def test_click_download():
    # Connect to the application (replace 'app_name' with your application)
    app = Application().connect(title_re=".*Save As.*", class_name="#32770")

    # Get the Save As dialog
    save_as_dialog = app.window(title_re=".*Save As.*", class_name="#32770")

    # Ensure the dialog is active and visible
    save_as_dialog.set_focus()

    # Click on the Downloads icon (usually a tree item in the navigation pane)
    try:
        downloads_item = save_as_dialog.child_window(title="Downloads", control_type="TreeItem")
        downloads_item.click_input()
    except Exception as e:
        print(f"Failed to click on Downloads icon: {e}")

    # Optionally, add a small delay to observe the action
    time.sleep(2)
