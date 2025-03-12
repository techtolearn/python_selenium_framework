from pywinauto import Application
from pywinauto.timings import wait_until_passes
import time


def test_navigate_Folder():
    # Connect to the application (replace 'app_name' with your application)
    app = Application().connect(title_re=".*Save As.*", class_name="#32770")

    # Get the Save As dialog
    save_as_dialog = app.window(title_re=".*Save As.*", class_name="#32770")

    # Ensure the dialog is active and visible
    save_as_dialog.set_focus()

    # Locate the address bar in the Save As dialog
    address_bar = save_as_dialog.child_window(auto_id="1001", control_type="Edit")

    # Paste the directory URL into the address bar
    directory_url = "C:\\Users\\YourUsername\\Downloads"
    address_bar.set_edit_text(directory_url)

    # Press Enter to navigate to the pasted directory
    address_bar.type_keys("{ENTER}")

    # Optionally, add a small delay to observe the action
    time.sleep(2)