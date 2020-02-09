import datetime
from time import sleep
from Model.Console import Console
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Model.FileHandler import FileHandler

import csv

from Model.ScrapeHandler import ScrapeHandler


class YfHandler(ScrapeHandler):

    handler_name = "YfHandler"

    baseDate = datetime.date(1970, 1, 1)

    def __init__(self, ticker, date_of_interest = None):

        super().__init__(ticker, date_of_interest)

        self.startDate = datetime.date(1962, 1, 2)
        self.stopDate = datetime.datetime.now().date()

        self.yfStartDate = self.yfDateRepresentation(self.startDate)
        self.yfStopDate = self.yfDateRepresentation(self.stopDate)

        dividentHistoryUrl = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=div%7Csplit&filter=div&frequency=1d".format(self.ticker, self.yfStartDate, self.yfStopDate)

        self.dbs = {
            "DividendHistory": {"url": dividentHistoryUrl}
        }

    @staticmethod
    def yfDateRepresentation(date):
        diff = date - YfHandler.baseDate
        return diff.days*24*60*60

    def download(self, form):
        if self.workFromArchive is False:
            # Start Browser
            YfHandler.start_browser()
            # Set Browser download path
            YfHandler.set_browser_download_path(self.path)

            if form == "DividendHistory":
                self.download_dividend_history()
        else:
            Console.print(YfHandler, "Download disabled, working from archive: " + form + " of " + self.ticker)

    def download_dividend_history(self):
        url = self.dbs["DividendHistory"]["url"]
        filePath = self.get_file_path("DividendHistory")

        YfHandler.browser.get(url)

        try:
            okButton = self.get_browser().find_element_by_name("agree")
            okButton.click()
        except NoSuchElementException:
            print("No OK button found.")

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





