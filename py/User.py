import hashlib


class User:
    def __init__(self,userName,userEmail,userPassword,userType):
        self.__userName = userName
        self.__userEmail = userEmail
        self.__userPassword = self.passwdCheck(userPassword)
        self.__userType = userType

    def passwdCheck(self,passwd):
        if len(passwd)>10:
            m = hashlib.sha256(passwd.encode('ascii')).digest()
            return m
        else:
            return ''

    def __str__(self):
        return self.__userName+' '+self.__userEmail+' '+self.__userType

class Buyer(User):
    def __init__(self,userName,userEmail,userPassword):
        super().__init__(userName,userEmail,userPassword,'buyer')

    def buyerDelete(self):
        return 0

class Seller(User):
    def __init__(self,userName,userEmail,userPassword):
        super().__init__(userName,userEmail,userPassword,'seller')

    def sellerDelete(self):
        return 0

class Staff(User):
    def __init__(self,userName,userEmail,userPassword):
        super().__init__(userName,userEmail,userPassword,'userType')

    def staffDelete():
        return 0
