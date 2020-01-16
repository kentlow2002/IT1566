# step in db
class Order:
    def __init__(self, orderId, orderDate, orderDesc, orderStatus, orderAddr, orderPrice, orderQuan):
        self.__orderList = []
        self.__orderId = 0 # to differentiate same products but bought by different users
        self.__orderDate = orderDate
        self.__orderDesc = orderDesc
        self.__orderStatus = orderStatus
        self.__orderAddr = orderAddr
        self.__orderPrice = orderPrice
        self.__orderQuan = orderQuan

    def get_orderDate(self):
        return self.__orderDate

    def get_orderPrice(self):
        return self.__orderPrice

    def get_orderQuan(self):
        return self.__orderQuan
