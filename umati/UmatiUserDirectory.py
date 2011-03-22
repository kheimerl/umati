import os.path
import pickle, time, re, logging
from . import Util

class User:
    
    def __init__(self, tag, creds, db):
        self.tag = tag
        self.__credits = creds
        self.init_done = False
        self.tasks_completed = {}
        self.gold_wrong = 0

    def getCredits(self):
        return self.__credits

    def task_completed(self, task):
        if (task):
            if (task.prelim == "true"):
                self.init_done = True
            if (task.isGold() and not task.isCorrect()):
                self.gold_wrong += 1
            if task.getType() not in self.tasks_completed:
                self.tasks_completed[task.getType()] = []
            self.tasks_completed[task.getType()].append(
                (task.getName(), task.getAns(), time.time()))
            self.change_credits(task.getValue())

    def get_tasks_completed(self, task_type):
        if task_type in self.tasks_completed:
            return self.tasks_completed[task_type]
        else:
            return []

    def __repr__(self):
        return str("Name: %s Credits: %d Init:%s Tasks:%s"
                   % (self.tag, self.__credits,
                      str(self.init_done), 
                      str(self.tasks_completed)))

    def change_credits(self, price):
        self.__credits += price

class UserDirectory:

    FILE_LOC = "umati_user_db"

    CAL_ID_RE = re.compile("(\s*);(\d+)=(/d+)?")

    def __init__(self, conf):
        self.path = conf.getAttribute("loc")
        self.max_wrong = int(conf.getAttribute("max_fails"))
        self.log = logging.getLogger("umati.UmatiUserDirectory.UserDirectory")
        if (self.path == ""):
            self.path = UserDirectory.FILE_LOC

        if (os.path.exists(self.path)):
            p = pickle.Unpickler(open(self.path, 'rb'))
            self.db = p.load()
        else:
            self.db = {}

    def get_user(self, tag):
        if not(UserDirectory.CAL_ID_RE.match(tag) or len(tag) == 2):
            self.log.warn("Invalid card scanned:%s" % tag)
            return None
        if tag not in self.db:
            self.db[tag] = User(tag, 0, self)
        user = self.db[tag]
        if (self.user_good(user)):
            return user
        else:
            self.log.warn("Cheating user blocked:%s" % tag)
            return None

    def task_completed(self, user, task):
        user.task_completed(task)
        self.changed()

    def change_credits(self, user, creds):
        user.change_credits(creds)
        self.changed()

    def update_user(self, user):
        self.db[user.tag] = user

    def user_good(self, user):
        return (user.gold_wrong < self.max_wrong)
        
    def changed(self):
        p = pickle.Pickler(open(self.path, 'wb'))
        p.dump(self.db)
