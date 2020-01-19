from abc import ABC, abstractmethod
from datetime import date

from Model.Company import Company


class CompanyChecker(ABC):

    def __init__(self, company: Company):
        self.company = company

    @abstractmethod
    def check(self, company: Company):
        pass


class DgiChecker(CompanyChecker):

    def __init__(self, company: Company):
        super().__init__(company)
        self.dividendPaymentContinuity = 0
        self.dividendGrowthContinuity = 0
        self.dividends = []

    def check(self):

        d0 = date(1970, 1, 1)
        d1 = date(2020, 1, 19)
        delta = d1 - d0
        delta_in_seconds = delta.days*24*60*60
        print("delta in seconds: " + str(delta_in_seconds))

        return self.checkDividendContinuities()

    def checkDividendContinuities(self):
        self.dividends = self.company.getDividends()
        yearCnt = -1
        latestDividend = float("inf")

        for dividend in self.dividends:
            if latestDividend > dividend:
                latestDividend = dividend
                if dividend != 0.0:
                    yearCnt = yearCnt + 1
            else:
                break
            if dividend != 0.0:
                self.dividendPaymentContinuity = self.dividendPaymentContinuity + 1

        self.dividendGrowthContinuity = yearCnt

        latestDividend = float("inf")

        for dividend in self.dividends:
            if latestDividend < dividend:
                return False

        return True


