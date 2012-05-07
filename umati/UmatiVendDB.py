import os.path
import pickle
import logging

class VendItem:

    def __init__(self, name, location, price):
        self.name = name
        self.loc = location
        self.price = price

class VendDB:

    FILE_LOC = "umati_vend_db"

    def __init__(self, conf):
        path = conf.getAttribute("loc")
        self.log = logging.getLogger("umati.UmatiVendDB.VendDB")
        if (path == ""):
            path = VendDB.FILE_LOC
        
        if (os.path.exists(path)):
            p = pickle.Unpickler(open(path, 'rb'))
            self.db = p.load()
            for k in self.db.keys():
                self.log.info("%s:%s" % (k, self.db[k].price))
        else:
            raise Exception("Vend DB Not Found")

    def getPriceFromLocation(self, loc):
        loc = loc.lower()
        if loc not in self.db:
            return None
        else:
            return self.db[loc].price
