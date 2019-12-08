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


class ProductList:
    def __init__(self):
        self.__list = []

    def addProduct(self,productId):
        #self.__list.append(product)
        return 0
    '''def rmProduct(self):
            return 0
            this function is to remove product. commented away for consideration'''
