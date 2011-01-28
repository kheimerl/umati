import os.path
import pickle

class User:
    
    def __init__(self, tag, creds):
        self.tag = tag
        self.credits = creds
        self.surveyed = False

class UserDirectory:

    FILE_LOC = "umati_user_db"

    def __init__(self):
        if (os.path.exists(UserDirectory.FILE_LOC)):
            p = pickle.Unpickler(open(UserDirectory.FILE_LOC, 'rb'))
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
        p = pickle.Pickler(open(UserDirectory.FILE_LOC, 'wb'))
        p.dump(self.db)
