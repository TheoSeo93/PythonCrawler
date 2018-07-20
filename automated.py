import csv
import datetime
from datetime import timedelta
import os

import time
from apscheduler.schedulers.blocking import BlockingScheduler
import pyrebase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sched = BlockingScheduler()

# Automated Scheduling Version
# Updates the menu to the Firebase Storage every two days 

@sched.scheduled_job('interval', minutes=2880)
def job():
    DINING_URL = 'https://cafes.compass-usa.com/StonyBrook/_layouts/15/appredirect.aspx?redirect_uri=https%3A%2F%2Fphapps%2Ecompassappstore%2Ecom%2FWebtritionMenuWeb%2FHome%3FSPHostUrl%3Dhttps%253A%252F%252Fcafes%252Ecompass%252Dusa%252Ecom%252FStonyBrook%26SPHostTitle%3DStonyBrook%26SPAppWebUrl%3D%22%22%26SPLanguage%3Den%252DUS%26SPClientTag%3D3%26SPProductNumber%3D15%252E0%252E4569%252E1000%26lid%3DlidTmp%26SenderId%3DA83BDF150&client_id=i%3A0i%2Et%7Cms%2Esp%2Eext%7C91c95c41%2D3ecb%2D47ca%2Dbaf7%2D377e96b97518%402b6b3e6d%2D0394%2D45b8%2Db909%2D8aa0ca7d9340&anon=1'
    currentDate = datetime.datetime.today()
    f = open('test.txt', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter='\t')
    print("Extracting Driver..")

    config = {
        "apiKey": "APIKEY",  # webkey
        "authDomain": "crawling-569b7.firebaseapp.com",
        "databaseURL": "https://crawling-569b7.firebaseio.com",  # database url
        "storageBucket": "crawling-569b7.appspot.com",  # storage
        "serviceAccount": "credential.json"
    }
    firebase = pyrebase.initialize_app(config)
    chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script(
        "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

    driver.get(DINING_URL)

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    for date in daterange(currentDate, currentDate + datetime.timedelta(days=20)):
        dateString = date.strftime("%m/%d/%Y")
        print("Starting from " + dateString)
        e = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "datepicker-stonybrook")))

        e.clear()
        e.send_keys(dateString)
        e.send_keys(u'\ue007')
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "venueFilter")))
        venue = soup.find("select", {"id": "venueFilter"})

        options = venue.find_all("option")
        venues = [x.text for x in options]

        for venue_element in venues:

            e = Select(driver.find_element_by_id("venueFilter"))
            e.select_by_visible_text(venue_element)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$" + venue_element + "$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "periodFilter")))
            time.sleep(2)
            period = soup.find("select", {"id": "periodFilter"})
            options_period = period.find_all("option")
            periods = [x.text for x in options_period]
            time.sleep(2)
            for period_element in periods:
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$" + period_element + "$$$$$$$$$$$$$$$$$$$$$$$$$$$")

                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.ID, "periodFilter")))
                e = Select(driver.find_element_by_id("periodFilter"))
                e.select_by_visible_text(period_element)
                time.sleep(2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "menu-item-container")))
                temp_parent = soup.find("div", {'class': 'menu-item-container'})

                temp_menu = [element for element in
                             (temp_parent.find_all("div", {'data-bind': 'html:NameAndImagesHTML'}))]
                menu = []
                for element in temp_menu:
                    WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "menu-item-title-stonybrook")))
                    menu.append(element.find("div", {'class': 'menu-item-title-stonybrook'}).get_text())
                price = [element.get_text() for element in (temp_parent.find_all("div", {"data-bind": "text:price"}))]
                result = []
                dateRow = []
                venueRow = []
                periodRow = []
                count = len(menu)
                for i in range(0, count):
                    dateRow.append(dateString)
                    venueRow.append(venue_element)
                    periodRow.append(period_element)

                result.extend([list(a) for a in zip(dateRow, venueRow, periodRow, menu, price)])
                for element in result:
                    print(element)
                    wr.writerow(element)

    f.close()
    driver.close()
    uploadfile = "test.txt"
    storage = firebase.storage()
    try:
        storage.child("test.txt").delete(uploadfile)
    except:
        storage.child("test.txt").put(uploadfile)


sched.start()
