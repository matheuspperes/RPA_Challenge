from playwright.sync_api import Playwright, sync_playwright
from time import sleep


items = [{'first_name': 'John', 'last_name': 'Smith', 'company': 'IT Solutions', 'role': 'Analyst', 'address': '98 North Road', 'email': 'jsmith@itsolutions.co.uk', 'phone': "40716543298"},
{'first_name': 'Jane', 'last_name': 'Dorsey', 'company': 'MediCare', 'role': 'Medical Engineer', 'address': '11 Crown Street', 'email': 'jdorsey@mc.com', 'phone': "40791345621"},
{'first_name': 'Albert', 'last_name': 'Kipling', 'company': 'Waterfront', 'role': 'Accountant', 'address': '22 Guild Street', 'email': 'kipling@waterfront.com', 'phone': "40735416854"},
{'first_name': 'Michael', 'last_name': 'Robertson', 'company': 'MediCare', 'role': 'IT Specialist', 'address': '17 Farburn Terrace', 'email': 'mrobertson@mc.com', 'phone': "40733652145"},
{'first_name': 'Doug', 'last_name': 'Derrick', 'company': 'Timepath Inc.', 'role': 'Analyst', 'address': '99 Shire Oak Road', 'email': 'dderrick@timepath.co.uk', 'phone': "40799885412"},
{'first_name': 'Jessie', 'last_name': 'Marlowe', 'company': 'Aperture Inc.', 'role': 'Scientist', 'address': '27 Cheshire Street', 'email': 'jmarlowe@aperture.us', 'phone': "40733154268"},
{'first_name': 'Stan', 'last_name': 'Hamm', 'company': 'Sugarwell', 'role': 'Advisor', 'address': '10 Dam Road', 'email': 'shamm@sugarwell.org', 'phone': "40712462257"},
{'first_name': 'Michelle', 'last_name': 'Norton', 'company': 'Aperture Inc.', 'role': 'Scientist', 'address': '13 White Rabbit Street', 'email': 'mnorton@aperture.us', 'phone': "40731254562"},
{'first_name': 'Stacy', 'last_name': 'Shelby', 'company': 'TechDev', 'role': 'HR Manager', 'address': '19 Pineapple Boulevard', 'email': 'sshelby@techdev.com', 'phone': "40741785214"},
{'first_name': 'Lara', 'last_name': 'Palmer', 'company': 'Timepath Inc.', 'role': 'Programmer', 'address': '87 Orange Street', 'email': 'lpalmer@timepath.co.uk', 'phone': "40731653845"}]

def start(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rpachallenge.com/")
    page.get_by_role("button", name="Start").click()
    
    for item in items:
        page.locator('rpa1-field[ng-reflect-dictionary-value="First Name"] input').fill(item["first_name"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Last Name"] input').fill(item["last_name"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Company Name"] input').fill(item["company"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Role in Company"] input').fill(item["role"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Address"] input').fill(item["address"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Email"] input').fill(item["email"])
        page.locator('rpa1-field[ng-reflect-dictionary-value="Phone Number"] input').fill(item["phone"])
        
        page.get_by_role("button", name="Submit").click()

    # ---------------------
    sleep(5)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    start(playwright)
