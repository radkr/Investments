import datetime
from abc import ABC, abstractmethod

from Model.FmpHandler import FmpHandler
from Model.YfHandler import YfHandler


class Company(ABC):

    def __init__(self, ticker, date_of_interest=None):

        self.ticker = ticker

        if date_of_interest is None:
            self.date = datetime.datetime.now().date()
        else:
            self.date = date_of_interest

        self.reports = {}

    @abstractmethod
    def getDividends(self):
        pass


class CompositeCompany(Company):

    def __init__(self, ticker, date_of_interest=None):

        super().__init__(ticker, date_of_interest)

        self.fmp_handler = FmpHandler(ticker, date_of_interest)
        self.yf_handler = YfHandler(ticker, date_of_interest)

    def getDividends(self):

        return self.yf_handler.get_form("DividendHistory")
