import shelve
import User as u


db = shelve.open('Users.db','c')
admin = u.Staff("adminadmin","limwenda@gmail.com","adminadmin",0)
buyer = u.Buyer("kentlow2002","kentlow2002@gmail.com","kentlow2002",1)
seller = u.Seller("matthiaschew681","matthiaschew681@gmail.com","matthiaschew681",2)
usersDict = {}
usersDict[0] = admin
usersDict[1] = buyer
usersDict[2] = seller
db['Users'] = usersDict
db.close()
db = shelve.open('Tokens.db','c')
tokensDict = {}
db['Tokens'] = tokensDict
db.close()
