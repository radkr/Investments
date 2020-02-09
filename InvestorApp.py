from Model.Company import CompositeCompany
from Model.CompanyChecker import DgiChecker
from Model.FileHandler import FileHandler
from Model.FmpHandler import FmpHandler
from Model.YfHandler import YfHandler

import csv
import datetime

if __name__ == '__main__':

    company = CompositeCompany("AAPL")

    dgiChecker = DgiChecker(company)
    dgiChecker.check()

    print(company.reports["dgi"])



