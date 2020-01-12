from Model.FmpHandler import FmpHandler


if __name__ == '__main__':
    handler = FmpHandler("AAPL")
    handler.downloadAll()
    handler.cacheAll()
    handler.save()
    handler.getForm("Profile")
    Profile = handler.getForm("Profile")
    print(Profile)
