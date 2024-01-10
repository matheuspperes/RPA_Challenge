from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from datetime import datetime
from pathlib import Path
from PIL import Image
from waits import Waits
from time import sleep
import pytesseract
import re


class Invoice:
    def start(self):
        self.final_data = {}
        service_chrome = ServiceChrome(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service_chrome)
        self.base_path = str(Path(__file__).parent)
        self.waits = Waits()

        driver.get('https://rpachallengeocr.azurewebsites.net/')
        driver.maximize_window()
       
        btn_start = driver.find_element(By.ID, "start")
        driver.execute_script("arguments[0].scrollIntoView()", btn_start)
        btn_start.click()
        sleep(0.5)
        
        driver.execute_script("window.scrollTo(1000, 0)")
        rows = self.waits.wait_all_presence({'css_selector': 'tr[role="row"]'}, driver)
        rows.pop(0)

        counter = 0
        for x in range(3):
            counter = self.validate_date_and_download_files(rows, counter)
            driver.find_element(By.CSS_SELECTOR, 'a[id="tableSandbox_next"]').click()
            rows = driver.find_elements(By.CSS_SELECTOR, 'tr[role="row"]')
            rows.pop(0)

        self.extract_ocr(counter)
        self.write_file()
        self.send_file(driver)
        
        sleep(4)
        driver.quit()
        return

    def validate_date_and_download_files(self, rows, counter):
        for row in rows:
            date = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            now = datetime.now()
            format_date = datetime.strptime(date, '%d-%m-%Y')

            if format_date <= now:
                counter += 1

                index = str(row.find_element(By.CSS_SELECTOR,'td:nth-child(2)').text).strip()
                invoice = row.find_element(By.CSS_SELECTOR, 'a')

                href = invoice.get_attribute('href')
                
                documents_path = Path(self.base_path, "documents")
                if not documents_path.exists():
                    documents_path.mkdir()
                    
                urlretrieve(href, Path(self.base_path, "documents", f"{str(counter)}.jpg"))
                self.final_data[f"{str(counter)}"] = {"index": index, "due_date": date}

            else:
                continue

        return counter

    def extract_ocr(self, number):
        data = []
        for index in range(1, number + 1):
            img = Image.open(str(Path(self.base_path, "documents", f"{index}.jpg")))
            data = pytesseract.image_to_string(img)

            name_1 = re.search(r"Aenean LLC", data)
            name_2 = re.search(r"Sit Amet Corp.", data)
            invoice_number = re.search(r"#( )?\d+", data)
            date_1 = re.search(r"(\D){3} (\d){1,2}, \d+", data)
            date_2 = re.search(r"(\d){4}-(\d){2}-(\d){2}", data)
            total = re.search(r"Total(:)? (\$)?\d+(.)?(\d){2}", data)

            invoice_number = str(invoice_number.group())[1:].strip()
            total = str(total.group())[6:].strip().replace('$', '')
            if name_1:
                name = name_1.group()
            else:
                name = name_2.group()

            if date_1:
                date = datetime.strptime(date_1.group(), '%b %d, %Y').strftime('%d-%m-%Y')
            else:
                date = datetime.strptime(date_2.group(), '%Y-%m-%d').strftime('%d-%m-%Y')
                
            self.final_data[str(index)]['invoice_number'] = invoice_number
            self.final_data[str(index)]['date'] = date
            self.final_data[str(index)]['name'] = name
            self.final_data[str(index)]['total'] = total
        return

    def write_file(self):
        with open('result.csv', mode='w+') as file:
            file.write('ID,DueDate,InvoiceNo,InvoiceDate,CompanyName,TotalDue')
            file.write('\n')
            
            for document in self.final_data:
                line = []
                for key in self.final_data[document].keys():
                    line.append(self.final_data[document][key])
                line = ','.join(line)
                file.write(line + '\n')
        return
    
    def send_file(self, driver):
        submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        submit_btn.send_keys(str(Path(self.base_path, "result.csv")))
        return

if __name__ == "__main__":
    bot = Invoice()
    bot.start()