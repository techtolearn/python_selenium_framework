# Pytest Selenium Framework

## Install on virtual environment

    $ git clone https://github.com/daniel-ob/pytest-selenium-framework.git
    $ cd pytest-selenium-framework
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt


## Run tests

    (venv)$ python -m pytest --html=reports/report.html


## Project folder structure

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
    │─── 📜 .ignore                 # Add Unwanted Files/Folders to .gitignore

## Git flow: 

    Initialize Git in Your Project Folder
        once above folder structure has created, click on terminal in pgit add .gitignoreycharm
        git init
    
    Add Remote Repository (GitHub/GitLab/Bitbucket, etc.)
        go to GitHub/GitLab and create a new repo
    
    push an existing repository from the command line
        git remote add origin https://github.com/techtolearn/python_selenium_framework.git
        git branch -M main  # Ensure you're on the main branch
        git add .
        git commit -m "first commit"
        git push -u origin main
        
    create your local branch to work and commit to main:
        git checkout -b <your-branch-name>   # Ensure you're on the your-branch-name
        git merge main
        git status
        Add your code
        git add .
        git commit -m "comment"
        git push --set-upstream origin <your-branch-name>

    Create a pull request for 'systemTesting' on GitHub by visiting:
    Login to git and click on repo - check Compare & pull request button appeared
         click on 'Compare & pull request' button
         click on 'Create pull request'
         click on 'Merge pull request'
         click on 'Confirm merge'
     Pull the Latest main Branch    
        git checkout main
        git pull origin main

### Key Note:

    when you want add a file and get the warning like below, simply execute the following commanad
    PS C:\Users\satyi\PycharmProjects\python_selenium_framework> git add .
   
     warning: in the working copy of '.idea/inspectionProfiles/profiles_settings.xml', LF will be replaced by CRLF the next time Git touches it
        git config --global core.autocrlf true


## File deletion: 
    e.g. git rm --cached <filename>.ini


## Adding libraries
    pip install selenium 
    
    if pip is not recognizing means, path of pip.exe is not added into the environment variable
    note: add this in system environment variable as path [pip,exe present under Scripts]
    C:\Users\YourUser\AppData\Local\Programs\Python\Python39\Scripts

    or 
    
py -m pip install <package_name>  #pip doesn't work


    Note: whenever you install the packages using pip- it doesn't track in the requirement.txt
    issue the below command to import

    pip freeze > requirements.txt


# PyTest Report:

    follow the instructions using below link to implement the report
        reference : 
                https://pytest-html.readthedocs.io/en/latest/user_guide.html
                https://docs.pytest.org/en/stable/how-to/output.html
                https://docs.pytest.org/en/stable/how-to/capture-warnings.html
                https://pytest-cov.readthedocs.io/en/latest/reporting.html
                https://pytest-with-eric.com/plugins/pytest-html/#Conclusion

## HTML Reports with pytest-html

    pip install pytest-html

## Run Tests with HTML Report Generation:

    pytest --html=reports/report.html

## Add Metadata for Better Reporting: In your conftest.py, include:
    import pytest
    def pytest_html_report_title(report):
    report.title = "Selenium Automation Test Report"

## To generate report in this framework

    - Run the test cases in tests folder 
    - open the terminal and follow the below commands
        C:\Users\satyi\PycharmProjects\python_selenium_framework\tests> pytest test_login.py
    - go to results folder under project folder to see the report.html

## Securely Store Passwords:

    1. Use Environment Variables (Recommended)
        Storing passwords in code is risky. Instead, store them securely using environment variables.
        Add your password to your system's environment variables:
       1.1. Windows
           setx PASSWORD "your_secure_password"
        1.2 Linux/Mac:
            export PASSWORD="your_secure_password"
       1.3. Access it in your config.py or login_page.py like this:
            import os
            PASSWORD = os.getenv("PASSWORD")
    
       2. Use .env Files (Alternative Approach)
           pip install python-dotenv 
       Create a .env file in your root folder:
           PASSWORD=your_secure_password
       Load it in config.py:
           from dotenv import load_dotenv
           import os
           load_dotenv()  # Load environment variables from .env file
           PASSWORD = os.getenv("PASSWORD")


## Recommended Improvements for Your Framework
    ✅ Use .env or environment variables for sensitive data.
    ✅ Leverage pytest.ini for better pytest configurations.
    ✅ Store report files in the /reports/ folder for easy tracking.
    ✅ For CI/CD integration, Allure is highly compatible with Jenkins, GitLab, etc.