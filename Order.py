class Order:
    def __init__(self,orderDict,orderId,orderDate,orderDesc,orderStatus,orderAddr,orderPrice,orderQuan,userId):
        self.__orderDict = orderDict
        self.__orderId = 0 #to differentiate same products but bought by different users
        self.__orderDate = orderDate
        self.__orderDesc = orderDesc
        self.__orderStatus = orderStatus
        self.__orderAddr = orderAddr
        self.__orderPrice = orderPrice
        self.__userId = userId

    def get_orderDict(self):
        return self.__orderDict
    def orderCancel(self):
        return 0
    def get_orderId(self):
        return self.__orderId
    def get_orderDate(self):
        return self.__orderDate
    def get_orderDesc(self):
        return self.__orderDesc
    def get_orderPrice(self):
        return self.__orderPrice
    def get_orderQuan(self):
        return self.__orderQuan
    def set_orderDesc(self, orderDesc):
        self.__orderDesc = orderDesc
    def get_orderStatus(self):
        return self.__orderStatus
    def set_orderStatus(self, orderStatus):
        self.__orderStatus = orderStatus
    def get_orderAddr(self):
        return self.__orderAddr
    def set_orderAddr(self,orderAddr):
        self.__orderAddr = orderAddr
    def get_userID(self):
        return self.__userId
