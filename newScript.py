import datetime
import math
from selenium import webdriver
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Enter total Orders
totalOrders = 12270
address_list = []
sku = ""
count = 0
try:
        
    # Start Chrome with remote debugging enabled
    subprocess.Popen(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"  --profile-directory="Profile 3" --remote-debugging-port=9222')
    time.sleep(10)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    driver = webdriver.Chrome(options=chrome_options)
    loopOrders = math.ceil(totalOrders / 15)
    for i in range(1, loopOrders):
        driver.get(f'https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page={i}&date-range=1673550000000-1677697198000')
        wait = WebDriverWait(driver, 1000)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'myo-table-container')))
        source_page = driver.page_source
        elements = driver.find_elements(By.XPATH,"//a[contains(@href,'/orders-v3/order/')]")
        hrefs = [element.get_attribute('href') for element in elements]
        for href in hrefs:
            print(href)
            driver.get(href)
            wait = WebDriverWait(driver, 1000)
            table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'a-keyvalue')))
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                for cell in cells:
                    if "SKU" in cell.get_attribute("innerHTML"):
                            sku = cell.text.split(': ')[-1]
                            print(sku)

            try:
                
                wait = WebDriverWait(driver, 1000)
                table = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-test-id='shipping-section-buyer-address']")))
                address_element = driver.find_element(By.XPATH,"//div[@data-test-id='shipping-section-buyer-address']")
                address = address_element.text
                address_split = address.split(', ')
                address_arr = [address_split[0]]+address_split[1].split(' ')            
                order_date_element = driver.find_element(By.XPATH,"//span[@data-test-id='order-summary-purchase-date-value']")
                address_data = address_arr + [sku]+[order_date_element.text]
                address_list.append(address_data)
                print(address_data)
                count += 1
                if (count == 100):
                     with open('address12.csv', mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for address in address_list:
                            try:
                                writer.writerow(address)
                            except Exception as e:
                                pass
                        address_list = []
                        count = 0
            except Exception as e:
                print(e)
except Exception as e:
    pass
