from abc import ABC, abstractmethod

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
        self.DividentGrowthContinuity = 0

    def check(self):
        return self.checkDividentGrowthContinuity()

    def checkDividentGrowthContinuity(self):
        dividends = self.company.getDividends()
        yearCnt = -1
        latestDividend = float("inf")

        for dividend in dividends:
            if latestDividend > dividend:
                latestDividend = dividend
                yearCnt = yearCnt + 1
            else:
                break

        self.DividentGrowthContinuity = yearCnt

        latestDividend = float("inf")

        for dividend in dividends:
            if latestDividend < dividend:
                return False

        return True


