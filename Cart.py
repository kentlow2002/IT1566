class Cart:
    def __init__(self, product):
        self.__cartProduct = product
        # self.__cartPrice = 0.00
        self.__cartQuantity = 0

    def get_cartPrice(self):
        return self.__cartPrice
    def get_cartQuantity(self):
        return self.__cartQuantity

    def addProduct(self,cartProduct):
        self.__cartDict[cartProduct.get_productId] = cartProduct

    def removeProduct(self,productId):
        self.__cartDict.pop(productId)

