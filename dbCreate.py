import shelve
import User as u


db = shelve.open('Users.db','c')
admin = u.Staff("adminadmin","admin@admin.admin","adminadminadmin",0)
usersDict = {}
usersDict[0] = admin
db['Users'] = usersDict
