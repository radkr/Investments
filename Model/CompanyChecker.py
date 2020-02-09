import math
from abc import ABC, abstractmethod
import datetime

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

        self.div_per_year = []
        self.div_payment_continuity = 0
        self.div_rise_continuity = 0
        self.div_payment_break_occurred = False
        self.div_rise_break_occurred = False
        self.div_reduction_occurred = False
        self.div_growth_rate = 0
        self.div_growth_rate_1y = 0
        self.div_growth_rate_3y = 0
        self.div_growth_rate_5y = 0
        self.div_growth_rate_10y = 0

    def check(self):

        self.calc_div_per_year()
        self.calc_div_continuities()
        self.calc_div_growth_rate()

        self.company.reports["dgi"] = {
            "div_per_year": self.div_per_year,
            "div_payment_continuity": self.div_payment_continuity,
            "div_rise_continuity": self.div_rise_continuity,
            "div_payment_break_occurred": self.div_payment_break_occurred,
            "div_rise_break_occurred": self.div_rise_break_occurred,
            "div_reduction_occurred": self.div_reduction_occurred,
            "div_growth_rate": self.div_growth_rate,
            "div_growth_rate_1y": self.div_growth_rate_1y,
            "div_growth_rate_5y": self.div_growth_rate_5y,
            "div_growth_rate_3y": self.div_growth_rate_3y,
            "div_growth_rate_10y": self.div_growth_rate_10y,
        }

    def calc_div_growth_rate(self):

        latest_div = 0
        growth_sum = 0
        div_growth_rate = []

        for i in range(len(self.div_per_year)):

            div = self.div_per_year[i][1]

            if i >= 1:

                if self.div_payment_continuity >= i:

                    growth = latest_div/div-1
                    growth_sum += growth

                    if i == 1:
                        self.div_growth_rate_1y = growth_sum
                    if i == 3:
                        self.div_growth_rate_3y = growth_sum/3
                    if i == 5:
                        self.div_growth_rate_5y = growth_sum/5
                    if i == 10:
                        self.div_growth_rate_10y = growth_sum/10

                    div_growth_rate.append(growth)
                else:
                    break

            latest_div = div

        self.div_growth_rate = div_growth_rate


    def calc_div_continuities(self):

        # Take into consideration that the company may not have payed
        # dividend in the examined year.
        if 1 >= (self.company.date.year-self.div_per_year[0][0]):
            latest_year = self.div_per_year[0][0]+1
        else:
            latest_year = self.company.date.year+1
        latest_div = float("inf")

        div_payment_continuity = -1
        div_rise_continuity = -1
        div_payment_break_occurred = False
        div_rise_break_occurred = False
        div_reduction_occurred = False

        for item in self.div_per_year:
            year = item[0]
            div = item[1]

            if (latest_year-year) == 1:
                div_payment_continuity += 1

                if latest_div >= div:
                    if div_reduction_occurred is False and div_rise_break_occurred is False:
                        div_rise_continuity += 1

                if math.isclose(latest_div, div, rel_tol=1e-3):
                    div_rise_break_occurred = True

                if div > latest_div:
                    div_reduction_occurred = True

                latest_year = year
                latest_div = div
            else:
                div_payment_break_occurred = True
                break

        self.div_payment_continuity = div_payment_continuity
        self.div_rise_continuity = div_rise_continuity
        self.div_payment_break_occurred = div_payment_break_occurred
        self.div_rise_break_occurred = div_rise_break_occurred
        self.div_reduction_occurred = div_reduction_occurred

    def calc_div_per_year(self, closed_years_only=True):

        present_year = self.company.date.year
        form = self.company.getDividends()

        div_per_year = []

        if form is not None:
            div_in_form = form["historical"]

            year = present_year
            q_cnt = 0
            div = 0

            for i in range(len(div_in_form)):
                adj_div = float(div_in_form[i]["adjDividend"])
                date = datetime.datetime.strptime(div_in_form[i]["date"], '%Y-%m-%d').date()

                if year != date.year:
                    # Save yearly data
                    if q_cnt != 4:
                        if year == present_year:
                            if closed_years_only is False:
                                div = div/q_cnt*4
                                div_per_year.append((year, div))
                        else:
                            div_per_year.append((year, div))
                    else:
                        div_per_year.append((year, div))

                    # Initialize next year
                    year = date.year
                    q_cnt = 1
                    div = adj_div
                else:
                    q_cnt += 1
                    div += adj_div

        self.div_per_year = div_per_year



