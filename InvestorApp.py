from Model.CompanyChecker import DgiChecker
from Model.FmpHandler import FmpHandler


if __name__ == '__main__':
    handler = FmpHandler("AAPL")
    #handler.downloadAll()
    handler.cacheAll()
    handler.save()
    handler.getForm("Profile")

    dgiChecker = DgiChecker(handler)
    dgiChecker.check()
    print(dgiChecker.DividentGrowthContinuity)

    print(str(handler.getDividends()))
