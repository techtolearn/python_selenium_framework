import time

from pywinauto import Application


class window:
    @staticmethod
    def save_download_file(file_name,directory_url):
        # Connect to the application (replace 'app_name' with your application)
        app = Application().connect(title='Save As', class_name="#32770")

        # Get the Save As dialog
        save_as_dialog = app.window(titlee='Save As', class_name="#32770")

        # Uncomment the following lines to inspect dialog controls - here you can get the complete attribute tree
        # save_as_dialog.print_control_identifiers()

        # Ensure the dialog is active and visible
        save_as_dialog.set_focus()

        # Locate the address bar in the Save As dialog , filename should not have any extension
        address_bar = save_as_dialog.child_window(title=file_name, class_name="Edit")

        # Paste the directory URL into the address bar
        # director_url = "C:\\Users\\YourUserName\Downloads"
        address_bar.set_edit_text(directory_url)

        # Press Save button to navigated to the pasted directory
        save_button = save_as_dialog.child_window(title="&Save", class_name="Button")
        save_button.click()

        # Optionally, add a small delay to observe the action
        time.sleep(5)