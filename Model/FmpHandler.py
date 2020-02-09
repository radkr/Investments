import urllib.request
import datetime
import os

from Model.BaseHandler import BaseHandler
from Model.FileHandler import FileHandler
from Model.Console import Console


class FmpHandler(BaseHandler):

    handler_name = "FmpHandler"

    def __init__(self, ticker, date_of_interest=None):
        super().__init__(ticker, date_of_interest)

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
                "StockPriceChangeVolume": {"url": "https://financialmodelingprep.com/api/v3/historical-price-full/"+self.ticker},
                "DividendHistory": {"url": "https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/"+self.ticker},
                "SplitHistory": {"url": "https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/"+self.ticker}
                }

    def download(self, form):
        if self.workFromArchive is False:
            url = self.dbs[form]["url"]
            filePath = self.get_file_path(form)

            urllib.request.urlretrieve(url, filePath)
        else:
            Console.print(FmpHandler, "Download disabled, working from archive: " + form + " of " + self.ticker)

    def save(self):
        filePath = self.get_file_path("")

        FileHandler.write(filePath, self.dbs)

    def getDividends(self):
        form = self.get_form("IncomeAnnual")
        dividents = []
        if form is not None:
            for financials in form['financials']:
                dividents.append(float(financials['Dividend per Share']))

        return dividents