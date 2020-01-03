from flask_login import UserMixin

class Ticket:
    tixID = 0
    def __init__(self, qn, ans, type):
        Ticket.tixID += 1
        self.__tID = Ticket.tixID
        self.__qn = qn
        self.__ans = ans
        self.__type = type

    def getQn(self):
        return self.__qn

    def getAns(self):
        return self.__ans

    def getType(self):
        return self.__type

    def getTID(self):
        return self.__tID

    def setQn(self, qn):
        self.__qn = qn

    def setAns(self, ans):
        self.__ans = ans
