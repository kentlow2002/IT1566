import hashlib
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,username,userEmail,userPassword,userType,userID):
        self.__username = username
        self.__userEmail = userEmail
        self.__userPassword = self.passwdCheck(userPassword)
        self.__userType = userType
        self.__userID = userID

    def passwdCheck(self,passwd):
        m = hashlib.sha256(passwd.encode('ascii')).digest()
        return m

    def loginCheck(self,passwdInput):
        n = hashlib.sha256(passwdInput.encode('ascii')).digest()
        if n!=self.__userPassword:
            return 0
        else:
            return 1

    def setUsername(self,newUsername):
        self.__username = newUsername

    def setEmail(self,newUserEmail):
        self.__userEmail = newUserEmail

    def setPassword(self,newPassword):
        self.__userPassword = self.passwdCheck(newPassword)

    def setAddr(self,newAddr):
        self.__userAddr = newAddr

    def getUsername(self):
        return self.__username

    def getEmail(self):
        return self.__userEmail

    def getType(self):
        return self.__userType

    def getID(self):
        return self.__userID

    def getAddr(self):
        return self.__userAddr

    def get_id(self):
        return self.__userID

    def __str__(self):
        return self.__username+' '+self.__userEmail+' '+str(self.__userPassword)+' '+self.__userType+' '+str(self.__userID)

class Buyer(User):
    def __init__(self,username,userEmail,userPassword,userType,userID):
        super().__init__(username,userEmail,userPassword, userType,userID)
        self.__buyerAddr = ""

    def buyerDelete(self):
        return 0

    def setBuyerAddr(self,newAddr):
        self.__buyerAddr = newAddr

    def getBuyerAddr(self):
        return self.__buyerAddr

    def __str__(self):
        return super().__str__() + ' ' + self.__buyerAddr

class Seller(User):
    def __init__(self,username,userEmail,userPassword,userType,userID):
        super().__init__(username,userEmail,userPassword,userType,userID)

    def sellerDelete(self):
        return 0

class Staff(User):
    def __init__(self,username,userEmail,userPassword,userID):
        super().__init__(username,userEmail,userPassword,'Staff',userID)

    def staffDelete():
        return 0
