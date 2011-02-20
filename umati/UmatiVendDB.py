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
        if (os.path.exists(VendDB.FILE_LOC)):
            p = pickle.Unpickler(open(VendDB.FILE_LOC, 'rb'))
            self.db = p.load()
        else:
            self.db = {}

    def getPriceFromLocation(loc):
        if loc not in self.db:
            return None
        else:
            return self.db[loc]
