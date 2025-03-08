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
Git flow: 
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


#****************************Adding libraries****************************
    pip install selenium 
#if pip is not recognizing means, path of pip.exe is not added into the environment variable
#note: add this in system environment variable as path [pip,exe present under Scripts]
#C:\Users\YourUser\AppData\Local\Programs\Python\Python39\Scripts

or 
    py -m pip install <package_name>  #pip doesn't work


Note: whenever you install the packages using pip- it doesn't track in the requirement.txt
sue the below command to import
    pip freeze > requirements.txt