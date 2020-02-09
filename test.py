import User as u
import shelve


db = shelve.open('Users.db','r')
usersDict = db['Users']
userEmail = 'test@alpha.com.sg'

for i in usersDict:
    print(usersDict[i].getEmail())
    if usersDict[i].getEmail() == userEmail:
        print('yes')
        break
    else:
        print('no')
