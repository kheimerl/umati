from . import UmatiMainWindow, Util, UmatiUpdater, UmatiUserDirectory
from PyQt4 import QtGui, QtCore
import sys

built = False

class Controller(QtCore.QObject):

    def __init__(self, surveyLoc, mathLoc):
        global built
        QtCore.QObject.__init__(self)
        #enforcing singleton
        if (built):
            raise Exception("Attempted to instantiate multiple umati controllers")
        else:
            built = True
        Util.setUmatiController(self)
        self.app = QtGui.QApplication(sys.argv)
        self.up = UmatiUpdater.NetworkUpdater(self)
        self.mw = UmatiMainWindow.MainWindow(surveyLoc = surveyLoc, mathLoc = mathLoc)
        self.db = UmatiUserDirectory.UserDirectory()

    def start(self):
        self.mw.show()
        self.up.start()
        sys.exit(self.app.exec_())

    def task_completed(self, task, value, reset=True):
        self.user.credits += value
        self.mw.setCredits(self.user.credits)
        if (reset):
            self.mw.setChooserVisible()

    def new_connection(self, tag):
        #here we check if the tag is new or not, eventually
        self.user = self.db.get_user(tag)
        if (self.user.surveyed):
            self.mw.setCredits(self.user.credits)
            self.mw.setChooserVisible()
        else:
            self.mw.setSurveyVisible()
        
    def timeout(self):
        self.user = None
        self.mw.setSplashVisible()
        
    def reset_countdown(self):
        self.up.reset_countdown()
