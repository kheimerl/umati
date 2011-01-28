from . import UmatiMainWindow, Util, UmatiUpdater
from PyQt4 import QtGui
import sys

built = False

class Controller():

    def __init__(self, surveyLoc, mathLoc):
        global built
        #enforcing singleton
        if (built):
            raise Exception("Attempted to instantiate multiple umati controllers")
        else:
            built = True
        Util.setUmatiController(self)
        self.app = QtGui.QApplication(sys.argv)
        self.mw = UmatiMainWindow.MainWindow(surveyLoc = surveyLoc, mathLoc = mathLoc)

        #this will be config set one day
        self.up = UmatiUpdater.NetworkUpdater(self)

    def start(self):
        self.mw.show()
        self.up.start()
        sys.exit(self.app.exec_())

    def task_completed(self, task, value, reset=True):
        self.mw.taskCompleted(value)
        if (reset):
            self.mw.setChooserVisible()

    def new_connection(self, tag):
        #here we check if the tag is new or not, eventually
        print (tag)
        self.mw.setChooserVisible()
        
    def timeout(self):
        self.mw.setSplashVisible()
        
    def reset_countdown(self):
        self.up.reset_countdown()
