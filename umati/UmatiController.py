from . import UmatiMainWindow, Util, UmatiUpdater, UmatiUserDirectory, UmatiVendDB
from PyQt4 import QtGui, QtCore
import sys, logging

module_built = False

PRICE = 5

class Controller(QtCore.QObject):

    def __init__(self, conf):
        global module_built
        QtCore.QObject.__init__(self)
        #enforcing singleton
        if (module_built):
            raise Exception("Attempted to instantiate multiple umati controllers")
        else:
            module_built = True
        self.log = logging.getLogger("umati.UmatiController.Controller")
        Util.setUmatiController(self)
        self.app = QtGui.QApplication(sys.argv)
        self.up = UmatiUpdater.Updater(self, Util.get_tag(conf, "updater"))
        self.mw = UmatiMainWindow.MainWindow(Util.get_tag(conf, "interface"))
        self.user_db = UmatiUserDirectory.UserDirectory(Util.get_tag(conf, "user_directory"))
        self.vend_db = UmatiVendDB.VendDB(Util.get_tag(conf, "vending"))

    def start(self):
        self.mw.show()
        self.up.start()
        sys.exit(self.app.exec_())

    def __update_user(self, task):
        self.user_db.task_completed(self.user, task)
        self.mw.setCredits(self.user.credits)

    def vendItem(self, target):
        price = self.vend_db.getPriceFromLocation(target)
        if (price and 
            self.user.credits >= price):
            self.db.change_credits(self.user, -price)
            self.mw.setCredits(self.user.credits)
            #could also check if item in stock here
            Util.sendVendCmd(target)
            return True
        else:
            if not price:
                self.log.info("Item not vended, not found: %s" % target)
            else:
                self.log.info("Item not vended, no credits: %s" % target)
            return False

    def task_completed(self, task, reset=True):
        self.__update_user(task)
        if not (self.user_db.user_good(self.user)):
            self.boot_user()
            return False
        elif (reset):
            self.choose_task()
            return False
        return True

    def get_completed_tasks(self, task_type):
        if (self.user):
            return self.user.get_tasks_completed(task_type)
        else:
            return None

    def choose_task(self):
        self.mw.setChooserVisible()

    def new_connection(self, tag):
        self.user = self.user_db.get_user(tag)
        if (self.user):
            self.mw.setCredits(self.user.credits)
            if (self.user.init_done):
                self.mw.setChooserVisible()
            else:
                self.mw.setPrelimVisible()
        else:
            self.boot_user()
        
    def timeout(self):
        self.user = None
        self.mw.setSplashVisible()

    def boot_user(self):
        self.mw.information("You have been removed from the system for violations of the 'be awesome' code.")
        self.timeout()
        
    def reset_countdown(self):
        self.up.reset_countdown()
