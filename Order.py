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
