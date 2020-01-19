import datetime
import os
import urllib
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Model.FileHandler import FileHandler
from bs4 import BeautifulSoup


class YfHandler:

    baseDate = datetime.date(1970, 1, 1)

    def __init__(self, ticker):
        self.ticker = ticker
        date = datetime.datetime.now().date()
        self.path = os.getcwd()

        self.path = self.path + "\\" + "YfHandler"
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + str(date)
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + ticker
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\"

        self.startDate = datetime.date(1962, 1, 2)
        self.stopDate = datetime.datetime.now().date()

        self.yfStartDate = self.yfDateRepresentation(self.startDate)
        self.yfStopDate = self.yfDateRepresentation(self.stopDate)

        dividentHistoryUrl = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=div%7Csplit&filter=div&frequency=1d".format(self.ticker, self.yfStartDate, self.yfStopDate)

        self.dbs = {
            "DividendHistory": {"url": dividentHistoryUrl}
        }

    def getFilePath(self, form):
        return self.path + self.ticker + "_" + form + ".json"

    @staticmethod
    def yfDateRepresentation(date):
        diff = date - YfHandler.baseDate
        return diff.days*24*60*60

    def getForm(self, form: str):
        if form == "DividendHistory":
            url = self.dbs[form]["url"]
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            browser.get(url)
            okButton = browser.find_element_by_name("agree")
            okButton.click()

            timeout = 5
            try:
                element_present = EC.presence_of_element_located((By.ID, 'element_id'))
                WebDriverWait(browser, timeout).until(element_present)
            except TimeoutException:
                print
                "Timed out waiting for page to load"

            element = browser.find_element_by_xpath("//a[@download='" + self.ticker + ".csv']")
            link = element.get_attribute("href")
            print(link)

            filePath = self.getFilePath(form)
            urllib.request.urlretrieve(link, filePath)



