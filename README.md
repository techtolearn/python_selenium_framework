selenium_pom_framework/
│─── 📂 tests/                  # Test Cases
│    │─── test_login.py         # Example test case
│    │─── test_checkout.py      # Example test case
│
│─── 📂 pages/                  # Page Object Model (POM) Classes
│    │─── base_page.py          # Base Page (common actions)
│    │─── login_page.py         # Login Page (locators & actions)
│    │─── home_page.py          # Home Page (locators & actions)
│
│─── 📂 locators/               # Locators stored separately
│    │─── login_locators.py     # Login Page locators
│    │─── home_locators.py      # Home Page locators
│
│─── 📂 utils/                  # Utility functions
│    │─── config.py             # Configuration settings (URLs, credentials)
│    │─── logger.py             # Logging mechanism
│    │─── data_reader.py        # Read test data from JSON, Excel, etc.
│
│─── 📂 test_data/              # Test Data
│    │─── login_data.json       # Example test data
│
│─── 📂 reports/                # Test Reports (Allure, HTML)
│
│─── 📂 drivers/                # WebDriver Executables (Optional)
│
│─── 📂 config/                 # Configuration Files
│    │─── config.yaml           # Global configurations
│
│─── 📂 resources/              # Static resources (if needed)
│
│─── 📜 conftest.py             # Pytest Fixtures (browser setup, teardown)
│─── 📜 requirements.txt        # Dependencies (selenium, pytest, allure, etc.)
│─── 📜 pytest.ini              # Pytest Configuration
│─── 📜 README.md               # Project Documentation

Git flow: 
Initialize Git in Your Project Folder
    once above folder structure has created, click on terminal in pycharm
    git init

Add Remote Repository (GitHub/GitLab/Bitbucket, etc.)
    go to GitHub/GitLab and create a new repo

push an existing repository from the command line
    git remote add origin https://github.com/techtolearn/python_selenium_framework.git
    git branch -M main
    git push -u origin main
    git remote add origin https://github.com/techtolearn/python_selenium_framework.git
    