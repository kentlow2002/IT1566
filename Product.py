import random as rand


class Product:
    countId = 0

    def __init__(self, productName, productCondition, productPrice, productQuantity, productDescription, productPicture, userID):
        Product.countId += 1
        self.__productId = Product.countId  # differentiates products with same name
        self.__productName = productName
        self.__productCondition = productCondition
        self.__productQuantity = productQuantity
        self.__productPrice = productPrice
        self.__productDescription = productDescription
        self.__productPicture = productPicture
        self.__productStatus = "public"
        self.__userID = int(userID)

    def productBuy(self):
        return 0

    def productSell(self):
        return 0

    # accessor

    def get_productId(self):
        return self.__productId

    def get_productName(self):
        return self.__productName

    def get_productCondition(self):
        return self.__productCondition

    def get_productQuantity(self):
        return self.__productQuantity

    def get_productPrice(self):
        return self.__productPrice

    def get_productDescription(self):
        return self.__productDescription

    def get_productPicture(self):
        return self.__productPicture

    def get_productStatus(self):
        return self.__productStatus

    def get_userID(self):
        return self.__userID

    # accessor

    def set_productId(self, productId):
        self.__productId = productId

    def set_productName(self, productName):
        self.__productName = productName

    def set_productCondition(self, productCondtion):
        self.__productCondition = productCondtion

    def set_productQuantity(self, productQuantity):
        self.__productQuantity = productQuantity

    def set_productPrice(self, productPrice):
        self.__productPrice = productPrice

    def set_productDesc(self, productDescription):
        self.__productDescription = productDescription

    def set_productPicture(self, productPicture):
        self.__productPicture = productPicture

    def set_productStatusPublic(self):
        self.__productStatus = "public"

    def set_productStatusHidden(self):
        self.__productStatus = "hidden"
