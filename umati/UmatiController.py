from . import UmatiMainWindow, Util, UmatiUpdater, UmatiUserDirectory
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
        self.up = UmatiUpdater.KeyboardUpdater(self)
        self.mw = UmatiMainWindow.MainWindow(conf)
        self.db = UmatiUserDirectory.UserDirectory()

        #this will be moved to it's own class
        self.set_prices()

    #from conf eventually
    def set_prices(self):
        self.prices = {}
        for let  in ['A', 'B', 'C', 'D', 'E', 'F']:
            for num in list(map(str, range(1,11))):
                self.prices[let+num] = PRICE

    def start(self):
        self.mw.show()
        self.up.start()
        sys.exit(self.app.exec_())

    def __update_user(self, task, value):
        self.user.credits += value
        if (task and task.type == "preliminary"):
            self.user.init_done = True
        self.db.changed()
        self.mw.setCredits(self.user.credits)

    def vendItem(self, target):
        if (target in self.prices and 
            self.user.credits >= self.prices[target]):
            self.__update_user(None, -(self.prices[target]))
            #could also check if item in stock here
            Util.sendVendCmd(target)
            return True
        else:
            return False

    def task_completed(self, task, value, reset=True):
        self.__update_user(task, value)
        if (reset):
            self.mw.setChooserVisible()

    def new_connection(self, tag):
        #here we check if the tag is new or not, eventually
        self.user = self.db.get_user(tag)
        self.mw.setCredits(self.user.credits)
        if (self.user.init_done):
            self.mw.setChooserVisible()
        else:
            self.mw.setPrelimVisible()
        
    def timeout(self):
        self.user = None
        self.mw.setSplashVisible()
        
    def reset_countdown(self):
        self.up.reset_countdown()
