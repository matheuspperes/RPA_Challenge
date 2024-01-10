from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


items = [{'first_name': 'John', 'last_name': 'Smith', 'company': 'IT Solutions', 'role': 'Analyst', 'address': '98 North Road', 'email': 'jsmith@itsolutions.co.uk', 'phone': 40716543298},
{'first_name': 'Jane', 'last_name': 'Dorsey', 'company': 'MediCare', 'role': 'Medical Engineer', 'address': '11 Crown Street', 'email': 'jdorsey@mc.com', 'phone': 40791345621},
{'first_name': 'Albert', 'last_name': 'Kipling', 'company': 'Waterfront', 'role': 'Accountant', 'address': '22 Guild Street', 'email': 'kipling@waterfront.com', 'phone': 40735416854},
{'first_name': 'Michael', 'last_name': 'Robertson', 'company': 'MediCare', 'role': 'IT Specialist', 'address': '17 Farburn Terrace', 'email': 'mrobertson@mc.com', 'phone': 40733652145},
{'first_name': 'Doug', 'last_name': 'Derrick', 'company': 'Timepath Inc.', 'role': 'Analyst', 'address': '99 Shire Oak Road', 'email': 'dderrick@timepath.co.uk', 'phone': 40799885412},
{'first_name': 'Jessie', 'last_name': 'Marlowe', 'company': 'Aperture Inc.', 'role': 'Scientist', 'address': '27 Cheshire Street', 'email': 'jmarlowe@aperture.us', 'phone': 40733154268},
{'first_name': 'Stan', 'last_name': 'Hamm', 'company': 'Sugarwell', 'role': 'Advisor', 'address': '10 Dam Road', 'email': 'shamm@sugarwell.org', 'phone': 40712462257},
{'first_name': 'Michelle', 'last_name': 'Norton', 'company': 'Aperture Inc.', 'role': 'Scientist', 'address': '13 White Rabbit Street', 'email': 'mnorton@aperture.us', 'phone': 40731254562},
{'first_name': 'Stacy', 'last_name': 'Shelby', 'company': 'TechDev', 'role': 'HR Manager', 'address': '19 Pineapple Boulevard', 'email': 'sshelby@techdev.com', 'phone': 40741785214},
{'first_name': 'Lara', 'last_name': 'Palmer', 'company': 'Timepath Inc.', 'role': 'Programmer', 'address': '87 Orange Street', 'email': 'lpalmer@timepath.co.uk', 'phone': 40731653845}]


def start():
    try:
        service_chrome = ServiceChrome(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service_chrome)

        driver.get('https://www.rpachallenge.com/')
        driver.maximize_window()

        driver.find_element(By.CSS_SELECTOR, 'button[class="waves-effect col s12 m12 l12 btn-large uiColorButton"]').click() # start_btn

        for item in items:
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Phone Number"] input').send_keys(item['phone']) # phone_number
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Role in Company"] input').send_keys(item['role']) # role
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Address"] input').send_keys(item['address']) # address
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Company Name"] input').send_keys(item['company']) # company
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="First Name"] input').send_keys(item['first_name']) # first_name
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Last Name"] input').send_keys(item['last_name']) # last_name
            driver.find_element(By.CSS_SELECTOR, 'rpa1-field[ng-reflect-dictionary-value="Email"] input').send_keys(item['email']) # email
            
            driver.find_element(By.CSS_SELECTOR, 'input[value="Submit"]').click() # submit_btn

        sleep(4)
        return 'Concluído com sucesso'
        
    except Exception as e:
        print(e)
        return 'Falha no processo'

if __name__ == '__main__':
    start()

