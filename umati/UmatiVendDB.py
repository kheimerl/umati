import os.path
import pickle

class VendItem:

    def __init__(self, name, location, price):
        self.name = name
        self.loc = location
        self.price = price

class VendDB:

    FILE_LOC = "umati_vend_db"

    def __init__(self, conf):
        path = conf.getAttribute("loc")
        if (path == ""):
            path = VendDB.FILE_LOC
        
        if (os.path.exists(path)):
            p = pickle.Unpickler(open(path, 'rb'))
            self.db = p.load()
        else:
            raise Exception("Vend DB Not Found")

    def getPriceFromLocation(self, loc):
        loc = loc.lower()
        print(loc)
        if loc not in self.db:
            return None
        else:
            return self.db[loc].price
