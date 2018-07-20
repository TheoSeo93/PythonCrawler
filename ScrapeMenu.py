import csv
import datetime
import time
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait

import pyrebase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# Firebase Version
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

options = Options()
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(chrome_options=options,
                          executable_path=r'/Users/ilsung/Desktop/project/chromedriver_win32/chromedriver.exe')
driver.set_window_size(1124, 850)
driver.implicitly_wait(3)
driver.get(DINING_URL)
driver.implicitly_wait(3)

def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector(' * /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')
    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)
    # click the button to clear the cache
    time.sleep(1)
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


for date in daterange(currentDate, currentDate + datetime.timedelta(days=20)):
    dateString = date.strftime("%m/%d/%Y")
    print("Starting from " + dateString)
    driver.implicitly_wait(10)
    e = driver.find_element_by_id("datepicker-stonybrook")
    e.clear()
    e.send_keys(dateString)
    e.send_keys(u'\ue007')
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    venue = soup.find("select", {"id": "venueFilter"})
    options = venue.find_all("option")
    venues = [x.text for x in options]

    for venue_element in venues:

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        e = Select(driver.find_element_by_id("venueFilter"))
        e.select_by_visible_text(venue_element)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$" + venue_element + "$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        period = soup.find("select", {"id": "periodFilter"})
        options_period = period.find_all("option")
        periods = [x.text for x in options_period]
        time.sleep(2)
        for period_element in periods:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$" + period_element + "$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            e = Select(driver.find_element_by_id("periodFilter"))
            e.select_by_visible_text(period_element)

            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            temp_parent = soup.find("div", {'class': 'menu-item-container'})

            temp_menu = [element for element in (temp_parent.find_all("div", {'data-bind': 'html:NameAndImagesHTML'}))]
            menu = []
            for element in temp_menu:
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
    clear_cache(driver)
    driver.get(DINING_URL)
f.close()
driver.close()

uploadfile = "test.txt"
storage = firebase.storage()
try:
    storage.child("test.txt").delete(uploadfile)
except:
    storage.child("test.txt").put(uploadfile)
