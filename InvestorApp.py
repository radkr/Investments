from Model.CompanyChecker import DgiChecker
from Model.FmpHandler import FmpHandler
from Model.YfHandler import YfHandler

if __name__ == '__main__':
    handler = FmpHandler("AAPL")
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
    print(handler.dbs)
    handler.getForm("DividendHistory")
