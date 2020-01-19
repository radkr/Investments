import json
import os
from Model.Console import Console

class FileHandler:

    @staticmethod
    def createFolder(path):
        try:
            os.mkdir(path)
        except OSError:
            Console.print(FileHandler, "Creation of the directory %s failed" % path)
        else:
            Console.print(FileHandler, "Successfully created the directory %s " % path)

    @staticmethod
    def read(filePath, encoding=None):
        jsonString = FileHandler.readTextFile(filePath, encoding)

        if jsonString is not None:
            dictionary = json.loads(jsonString)
            return dictionary
        else:
            return None

    @staticmethod
    def write(filePath, dictionary, encoding='utf8'):

        jsonString = json.dumps(dictionary, sort_keys=True, indent=4,
                                separators=(',', ': '))

        FileHandler.writeTextFile(filePath, jsonString, encoding)

    @staticmethod
    def readTextFile(filePath, encoding=None):
        if os.path.isfile(filePath) is True:
            with open(filePath, 'rb') as textFile:
                rawData = textFile.read()
                textFile.close()
                if encoding is None:
                    encodings = ['utf8', 'cp1252', 'ascii', 'iso-8859-1', 'iso-8859-16']
                    for encoding in encodings:
                        try:
                            textData = rawData.decode(encoding)
                            break
                        except:
                            continue
                    else:
                        encoding = chardet.detect(rawData)['encoding']
                        try:
                            textData = rawData.decode(encoding)
                        except:
                            textData = ''
                else:
                    try:
                        textData = rawData.decode(encoding)
                    except:
                        textData = ''
                return textData
        else:
            return None

    @staticmethod
    def writeTextFile(filePath, text, encoding='utf8'):
        rawData = text.encode(encoding)

        with open(filePath, 'wb') as textFile:
            textFile.write(rawData)
        textFile.close()