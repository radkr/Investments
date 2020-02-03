import datetime
import os
from time import sleep
from Model.Console import Console

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Model.FileHandler import FileHandler

import csv


class YfHandler:

    baseDate = datetime.date(1970, 1, 1)
    browserUserCnt = 0
    browser = None

    def __init__(self, ticker, dateOfInterest = None):
        self.ticker = ticker

        if dateOfInterest is None:
            date = datetime.datetime.now().date()
        else:
            date = dateOfInterest

        if date == datetime.datetime.now().date():
            self.workFromArchive = False
        else:
            self.workFromArchive = True

        self.path = os.getcwd()

        self.path = self.path + "\\" + "YfHandler"
        if self.workFromArchive is False:
            FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + str(date)
        if self.workFromArchive is False:
            FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + ticker
        if self.workFromArchive is False:
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

        if self.workFromArchive is False:
            # Starting Browser if do not exist
            if YfHandler.browserUserCnt == 0:
                YfHandler.startBrowser()
            YfHandler.browserUserCnt = YfHandler.browserUserCnt + 1

            # Set Browser download path
            self.setBrowserDownloadPath()

    def __del__(self):
        YfHandler.browserUserCnt = YfHandler.browserUserCnt - 1
        if YfHandler.browserUserCnt == 0:
            YfHandler.stopBrowser()

    @staticmethod
    def startBrowser():
        options = webdriver.ChromeOptions()

        options.add_experimental_option("prefs", {
            "download.default_directory": "/path/to/download/dir",
            "download.prompt_for_download": False,
        })

        options.add_argument('--headless')

        YfHandler.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    @staticmethod
    def stopBrowser():
        YfHandler.browser.quit()

    def setBrowserDownloadPath(self):
        # add missing support for chrome "send_command"  to selenium webdriver
        YfHandler.browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.path}}
        command_result = YfHandler.browser.execute("send_command", params)

    def getFilePath(self, form):
        return self.path + self.ticker + "_" + form + ".json"

    @staticmethod
    def yfDateRepresentation(date):
        diff = date - YfHandler.baseDate
        return diff.days*24*60*60

    def download(self, form):
        if self.workFromArchive is False:
            if form == "DividendHistory":
                self.downloadDividendHistory()
        else:
            Console.print(YfHandler, "Download disabled, working from archive: " + form + " of " + self.ticker)

    def downloadDividendHistory(self):
        url = self.dbs["DividendHistory"]["url"]
        filePath = self.getFilePath("DividendHistory")

        YfHandler.browser.get(url)
        okButton = YfHandler.browser.find_element_by_name("agree")
        okButton.click()

        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'element_id'))
            WebDriverWait(YfHandler.browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        element = YfHandler.browser.find_element_by_xpath("//a[@download='" + self.ticker + ".csv']")

        element.click()
        # wait for download
        sleep(2)

        CsvFilePath = self.path + self.ticker + ".csv"

        Dividends = {}
        Dividends["symbol"] = self.ticker

        DividendList = []

        with open(CsvFilePath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Dividend = {}
                if line_count != 0:
                    date = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
                    Dividend["date"] = str(date)
                    Dividend["label"] = ""
                    Dividend["adjDividend"] = row[1]

                    if len(DividendList) == 0:
                        DividendList.insert(0, (date, Dividend))
                    else:
                        for i in range(len(DividendList)):
                            if date > DividendList[i][0]:
                                DividendList.insert(i, (date, Dividend))
                                break
                            else:
                                if i == len(DividendList) - 1:
                                    DividendList.append((date, Dividend))

                    line_count += 1
                else:
                    line_count += 1

        Dividends["historical"] = []

        for i in range(len(DividendList)):
            Dividends["historical"].append(DividendList[i][1])

        FileHandler.write(filePath, Dividends)

    def cache(self, form):
        filePath = self.getFilePath(form)

        if os.path.isfile(filePath) is True:
            value = FileHandler.read(filePath)
            self.dbs[form]["value"] = value
            return value
        else:
            return None

    def loadFromUrl(self, form):
        Console.print(YfHandler, "loadFromUrl: " + form + " of " + self.ticker)
        self.download(form)
        return self.cache(form)

    def loadFromFile(self, form):
        filePath = self.getFilePath(form)

        if os.path.isfile(filePath) is True:
            Console.print(YfHandler, "loadFromFile: " + form + " of " + self.ticker)
            return self.cache(form)
        else:
            return self.loadFromUrl(form)

    def loadFromCache(self, form):

        if "value" in self.dbs[form].keys():
            Console.print(YfHandler, "loadFromCache: " + form + " of " + self.ticker)
            return self.dbs[form]["value"]
        else:
            return self.loadFromFile(form)

    def getForm(self, form: str):
        return self.loadFromCache(form)





