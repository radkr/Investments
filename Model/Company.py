from abc import ABC, abstractmethod


class Company(ABC):

    @abstractmethod
    def getDividends(self):
        pass
