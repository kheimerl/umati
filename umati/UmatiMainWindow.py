from PyQt4 import QtGui, QtCore, uic
import logging

from . import UmatiChooserWidget
from . import UmatiVendWidget
from . import UmatiSplashWidget

WINDOW = None

def getMainWindow():
    global WINDOW
    if (WINDOW):
        return WINDOW
    else:
        raise Exception('No Main Window!')

UI_FILE = 'umati/UmatiMainView.ui'

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, surveyLoc = None, mathLoc = None):
        global WINDOW
        QtGui.QMainWindow.__init__(self)
        self.log = logging.getLogger("umati.UmatiMainWindow.MainWindow")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        
        #setup other parts
        self.chooser = UmatiChooserWidget.ChooserGui(self, mathLoc, surveyLoc, self.ui.BodyFrame)
        self.vend = UmatiVendWidget.VendGui(self, self.ui.BodyFrame)
        self.splash = UmatiSplashWidget.SplashGui(self, self.ui.BodyFrame)

        #start with splash screen
        self.setSplashVisible()
        
        self.ui.vendButton.clicked.connect(self.setVendVisible)
        self.ui.resetButton.clicked.connect(self.setChooserVisible)
        self.ui.full_screen.clicked.connect(self.fullScreen)

        WINDOW = self

    def fullScreen(self):
        self.ui.full_screen.hide()
        self.showFullScreen()

    def __setItemVisible(self, item, others):
        item.show()
        for other in others:
            other.hide()

    def setChooserVisible(self):
        self.ui.topFrame.show()
        self.ui.resetButton.hide()
        self.ui.vendButton.show()
        self.__setItemVisible(self.chooser, [self.vend, self.splash])

    def setVendVisible(self):
        self.ui.topFrame.show()
        self.ui.resetButton.show()
        self.ui.vendButton.hide()
        self.__setItemVisible(self.vend, [self.chooser, self.splash]) 

    def setSplashVisible(self):
        self.ui.topFrame.hide()
        self.__setItemVisible(self.splash, [self.vend, self.chooser])

    def vendItem(self, value):
        if (self.ui.lcdNumber.intValue() >= value):
            self.ui.lcdNumber.display(self.ui.lcdNumber.intValue() - value)
            return True
        return False

    def getValue(self):
        return self.ui.lcdNumber.intValue()

    def taskCompleted(self, value):
        self.ui.lcdNumber.display(self.ui.lcdNumber.intValue() + value)
