import random as rand


class Products:
    def __init__(self,productId,productName,productStock,productPrice,productDesc):
        self.__productId = 0 #differentiates products with same name
        self.__productName = productName
        self.__productStock = productStock
        self.__productPrice = productPrice
        self.__productDesc = productDesc

    def productBuy(self):
        return 0

    def productSell(self):
        return 0
    def get_productID(self):
        return self.__productId
    def get_productName(self):
        return self.__productName
    def set_productName(self, productName):
        self.__productName = productName
    def get_productStock(self):
        return self.__productStock
    def set_productStock(self, productStock):
        self.__productName = productStock
    def get_productPrice(self):
        return self.__productPrice
    def set_productPrice(self, productPrice):
        self.__productPrice = productPrice
    def get_productDesc(self):
        return self.__productDesc
    def set_productDesc(self, productDesc):
        self.__productDesc = productDesc
class ProductList:
    def __init__(self):
        self.__list = []

    def addProduct(self,productId):
        #self.__list.append(product)
        return 0
    '''def rmProduct(self):
            return 0
            this function is to remove product. commented away for consideration'''
