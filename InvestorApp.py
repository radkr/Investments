from Model.CompanyChecker import DgiChecker
from Model.FileHandler import FileHandler
from Model.FmpHandler import FmpHandler
from Model.YfHandler import YfHandler

import csv
import datetime

if __name__ == '__main__':
    #handler = FmpHandler("AAPL", datetime.date(1970, 1, 1))
    handler = FmpHandler("AAPL", datetime.datetime.now().date())
    #handler.downloadAll()
    handler.cacheAll()
    handler.save()
    handler.getForm("Profile")

    dgiChecker = DgiChecker(handler)
    dgiChecker.check()
    print(dgiChecker.dividendGrowthContinuity)
    print(dgiChecker.dividendPaymentContinuity)
    print(dgiChecker.dividends)

    handler = YfHandler("AAPL")
    form = handler.getForm("DividendHistory")
    print(form)



