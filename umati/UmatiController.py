from . import UmatiMainWindow, Util, UmatiUpdater
from PyQt4 import QtGui
import sys

class Controller():
    
    def __init__(self, surveyLoc, mathLoc):
#this is the controller in MVC right now, probably bad
        self.app = QtGui.QApplication(sys.argv)
        self.mw = UmatiMainWindow.MainWindow(surveyLoc = surveyLoc, mathLoc = mathLoc)

        self.up = UmatiUpdater.NetworkUpdater()

    def start(self):
        self.mw.show()
        self.up.start()
        sys.exit(self.app.exec_())

        

