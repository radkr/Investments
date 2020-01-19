import urllib.request
import datetime
import os
from Model.FileHandler import FileHandler
from Model.Console import Console
from Model.Company import Company


class FmpHandler(Company):

    def __init__(self, ticker):
        self.ticker = ticker
        date = datetime.datetime.now().date()
        self.path = os.getcwd()

        self.path = self.path + "\\" + "FmpHandler"
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + str(date)
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + ticker
        FileHandler.createFolder(self.path)
        self.path = self.path + "\\"

        self.dbs = {
                "Profile": {"url": "https://financialmodelingprep.com/api/v3/company/profile/"+self.ticker},
                "IncomeAnnual": {"url": "https://financialmodelingprep.com/api/v3/financials/income-statement/" + self.ticker},
                "IncomeQuarterly": {"url": "https://financialmodelingprep.com/api/v3/financials/income-statement/" + self.ticker + "?period=quarter"},
                "BalanceSheetAnnual": {"url": "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"+self.ticker},
                "BalanceSheetQuarterly": {"url": "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"+self.ticker+"?period=quarter"},
                "CashFlowAnnual": {"url": "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/"+self.ticker},
                "CashFlowQuarterly": {"url": "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/"+self.ticker+"?period=quarter"},
                "FinancialRatios": {"url": "https://financialmodelingprep.com/api/v3/financial-ratios/"+self.ticker},
                "EnterpriseValueAnnual": {"url": "https://financialmodelingprep.com/api/v3/enterprise-value/"+self.ticker},
                "EnterpriseValueQuarterly": {"url": "https://financialmodelingprep.com/api/v3/enterprise-value/"+self.ticker+"?period=quarter"},
                "KeyMetricsAnnual": {"url" :"https://financialmodelingprep.com/api/v3/company-key-metrics/"+self.ticker},
                "KeyMetricsQuarterly": {"url": "https://financialmodelingprep.com/api/v3/company-key-metrics/"+self.ticker+"?period=quarter"},
                "FinancialGrowthAnnual": {"url": "https://financialmodelingprep.com/api/v3/financial-statement-growth/"+self.ticker},
                "FinancialGrowthQuarterly": {"url": "https://financialmodelingprep.com/api/v3/financial-statement-growth/"+self.ticker+"?period=quarter"},
                "Dcf": {"url": "https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/"+self.ticker},
                "DcfAnnual": {"url": "https://financialmodelingprep.com/api/v3/company/historical-discounted-cash-flow/"+self.ticker},
                "DcfQuarterly": {"url": "https://financialmodelingprep.com/api/v3/company/historical-discounted-cash-flow/"+self.ticker+"?period=quarter"},
                "StockPrice": {"url": "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL"+self.ticker+"?serietype=line"},
                "StockPriceChangeVolume": {"url": "https://financialmodelingprep.com/api/v3/historical-price-full/"+self.ticker}
                }

    def getFilePath(self, form):
        return self.path + self.ticker + "_" + form + ".json"

    def download(self, form):
        url = self.dbs[form]["url"]
        filePath = self.getFilePath(form)

        urllib.request.urlretrieve(url, filePath)

    def downloadAll(self):

        for key in self.dbs.keys():
            self.download(key)

    def cache(self, form):
        filePath = self.getFilePath(form)

        if os.path.isfile(filePath) is True:
            value = FileHandler.read(filePath)
            self.dbs[form]["value"] = value
            return value
        else:
            return None

    def cacheAll(self):

        for key in self.dbs.keys():
            self.cache(key)

    def save(self):
        filePath = self.getFilePath("")

        FileHandler.write(filePath, self.dbs)

    def loadFromUrl(self, form):
        Console.print(FmpHandler, "loadFromUrl: " + form + " of " + self.ticker)
        self.download(form)
        return self.cache(form)

    def loadFromFile(self, form):
        filePath = self.getFilePath(form)

        if os.path.isfile(filePath) is True:
            Console.print(FmpHandler, "loadFromFile: " + form + " of " + self.ticker)
            return self.cache(form)
        else:
            return self.loadFromUrl(form)

    def loadFromCache(self, form):

        if "value" in self.dbs[form].keys():
            Console.print(FmpHandler, "loadFromCache: " + form + " of " + self.ticker)
            return self.dbs[form]["value"]
        else:
            return self.loadFromFile(form)

    def getForm(self, form):
        return self.loadFromCache(form)

    def getDividends(self):
        form = self.getForm("IncomeAnnual")
        dividents = []
        for financials in form['financials']:
            dividents.append(float(financials['Dividend per Share']))
        return dividents