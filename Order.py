class Order:
    def __init__(self,orderId,orderDate,orderDesc,orderStatus):
        self.__orderList = []
        self.__orderId = orderId
        self.__orderDate = orderDate
        self.__orderDesc = orderDesc
        self.__orderStatus = orderStatus

    def addProduct(self,productList):
        self.__orderList.append(productList)

    def orderCancel(self):
        return 0
    def get_orderId(self):
        return self.__orderId
    def get_orderDate(self):
        return self.__orderDate
    def get_orderDesc(self):
        return self.__orderDesc
    def set_orderDesc(self, orderDesc):
        self.__orderDesc = orderDesc
    def get_orderStatus(self):
        return self.__orderStatus
    def set_orderStatus(self, orderStatus):
        self.__orderStatus = orderStatus
