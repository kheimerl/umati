import os.path
import pickle, time

class User:
    
    def __init__(self, tag, creds, db):
        self.tag = tag
        self.credits = creds
        self.db = db
        self.init_done = False
        self.tasks_completed = {}

    def task_completed(self, task):
        if (task):
            self.changeCredits(task.getValue())
            if (task.prelim == "true"):
                self.init_done = True
            if task.getType() not in self.tasks_completed:
                self.tasks_completed[task.getType()] = []
            self.tasks_completed[task.getType()].append((task.getName(), task.getAns(), time.time()))
        self.db.changed()

    def __repr__(self):
        return str("Name: %s Credits: %d Init:%s Tasks:%s"
                   % (self.tag, self.credits,
                      str(self.init_done), 
                      str(self.tasks_completed)))

    def changeCredits(self, price):
        self.credits += price
        self.db.changed()

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
            self.db[tag] = User(tag, 0, self)
        return self.db[tag]

    def update_user(self, user):
        self.db[user.tag] = user

    def changed(self):
        p = pickle.Pickler(open(self.path, 'wb'))
        p.dump(self.db)
