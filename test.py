import User as u
import Product as p
import shelve


db = shelve.open('Orders.db','r')
ordersCount = db['count']
print(ordersCount)
