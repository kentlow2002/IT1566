import shelve
import Product as p
db = shelve.open("Products.db","c")
productsDict = {}
productsDict[0] = p.Product("test", "new", "10", "20", "test product", "qwe")
productsDict[1] = p.Product("lul", "new", "10", "30", "lul product", "rty")
productsDict[2] = p.Product("what", "new", "10", "40", "what product", "uiop")
db['Products'] = productsDict
db.close()
