import datetime
import os

from Model.Console import Console
from Model.FileHandler import FileHandler


class BaseHandler:

    handler_name = "BaseHandler"

    def __init__(self, ticker, date_of_interest=None):
        self.ticker = ticker

        if date_of_interest is None:
            date = datetime.datetime.now().date()
        else:
            date = date_of_interest

        if date == datetime.datetime.now().date():
            self.workFromArchive = False
        else:
            self.workFromArchive = True

        self.path = os.getcwd()

        self.path = self.path + "\\" + self.handler_name
        if self.workFromArchive is False:
            FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + str(date)
        if self.workFromArchive is False:
            FileHandler.createFolder(self.path)
        self.path = self.path + "\\" + ticker
        if self.workFromArchive is False:
            FileHandler.createFolder(self.path)
        self.path = self.path + "\\"

        self.dbs = {}

    def get_file_path(self, form):

        return self.path + self.ticker + "_" + form + ".json"

    def download_all(self):

        for key in self.dbs.keys():
            self.download(key)

    def cache(self, form):
        file_path = self.get_file_path(form)

        if os.path.isfile(file_path) is True:
            value = FileHandler.read(file_path)
            self.dbs[form]["value"] = value
            return value
        else:
            return None

    def cache_all(self):

        for key in self.dbs.keys():
            self.cache(key)

    def load_from_url(self, form):

        Console.print(self.__class__, "loadFromUrl: " + form + " of " + self.ticker)
        self.download(form)
        return self.cache(form)

    def load_from_file(self, form):

        filePath = self.get_file_path(form)

        if os.path.isfile(filePath) is True:
            Console.print(self.__class__, "loadFromFile: " + form + " of " + self.ticker)
            return self.cache(form)
        else:
            return self.load_from_url(form)

    def load_from_cache(self, form):

        if "value" in self.dbs[form].keys():
            Console.print(self.__class__, "loadFromCache: " + form + " of " + self.ticker)
            return self.dbs[form]["value"]
        else:
            return self.load_from_file(form)

    def get_form(self, form):

        return self.load_from_cache(form)
