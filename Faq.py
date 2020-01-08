from flask_login import UserMixin

class Ticket:
    def __init__(self, qn, ans, type, id, userID):
        self.__tID = id
        self.__qn = qn
        self.__ans = ans
        self.__type = type
        self.__userID = userID

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

    def getUID(self):
        return self.__userID
