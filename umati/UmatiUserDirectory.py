import os.path
import pickle, time, re, logging
from PyQt4.Qt import QThread, QMutex, QMutexLocker
from . import Util

class User(object):
    
    def __init__(self, tag, creds):
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

class UpdaterThread(QThread):
    
    def __init__(self, ud):
        QThread.__init__(self)
        self.daemon = True
        self.done = False
        self.ud = ud

    def run(self):
        while not (self.done):
            self.ud.dump()
            time.sleep(60)

class UserDirectory:

    FILE_LOC = "umati_user_db"

    CAL_ID_RE = re.compile("(\s*);(\d+)=(/d+)?")

    UPDATE_TIMEOUT = 60*10

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

        self.__lock = QMutex()
        self.__last_updated = time.time()
        self.__hasChanged = False
        self.updater = UpdaterThread(self)
        self.updater.start()

    def get_user(self, tag):
        QMutexLocker(self.__lock)
        res = None
        if not(UserDirectory.CAL_ID_RE.match(tag) or len(tag) == 2):
            self.log.warn("Invalid card scanned:%s" % tag)
        else:
            if tag not in self.db:
                self.log.info("New user %s" % tag)
                self.db[tag] = User(tag, 0)
            user = self.db[tag]
            if (self.user_good(user)):
                res = user
            else:
                self.log.warn("Cheating user blocked:%s" % tag)
        self.__changed()
        return res
        
    def task_completed(self, user, task):
        QMutexLocker(self.__lock)
        user.task_completed(task)
        self.__changed()

    def change_credits(self, user, creds):
        QMutexLocker(self.__lock)
        user.change_credits(creds)
        self.__changed()

    def update_user(self, user):
        QMutexLocker(self.__lock)
        self.db[user.tag] = user
        self.__changed()

    def user_good(self, user):
        return (user.gold_wrong < self.max_wrong)
        
    def __changed(self):
        self.__hasChanged = True
        self.__last_updated = time.time()

    def dump(self):
        QMutexLocker(self.__lock)
        if (self.__hasChanged and 
            self.__last_updated + UserDirectory.UPDATE_TIMEOUT < time.time()):
            self.log.info("DB Dumped")
            p = pickle.Pickler(open(self.path, 'wb'))
            p.dump(self.db)
            self.__hasChanged = False
            self.__last_updated = time.time()
