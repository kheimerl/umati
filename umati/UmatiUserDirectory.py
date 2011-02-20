import os.path
import pickle

class User:
    
    def __init__(self, tag, creds):
        self.tag = tag
        self.credits = creds
        self.init_done = False

class UserDirectory:

    FILE_LOC = "umati_user_db"

    def __init__(self, conf):
        self.path = conf.getAttribute("loc")
        if (self.path == ""):
            self.path = UserDirectory.FILE_LOC

        if (os.path.exists(self.path)):
            p = pickle.Unpickler(open(self.path, 'rb'))
            self.db = p.load()
        else:
            self.db = {}

    def get_user(self, tag):
        if tag not in self.db:
            self.db[tag] = User(tag, 0)
        return self.db[tag]

    def update_user(self, user):
        self.db[user.tag] = user

    def changed(self):
        p = pickle.Pickler(open(self.path, 'wb'))
        p.dump(self.db)
