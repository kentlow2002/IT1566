import User as u
import shelve


userDict = shelve.open('Users.db', 'r')['Users']
for i,j in userDict.items():
    print(i,j)
