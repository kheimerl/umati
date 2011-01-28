from PyQt4 import QtGui, QtCore, uic
import logging

from . import UmatiChooserWidget
from . import UmatiVendWidget
from . import UmatiSplashWidget
from . import UmatiSurveyTaskWidget

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
        self.chooser = UmatiChooserWidget.ChooserGui(mathLoc, parent = self.ui.BodyFrame)
        self.vend = UmatiVendWidget.VendGui(self, parent = self.ui.BodyFrame)
        self.splash = UmatiSplashWidget.SplashGui(self, parent = self.ui.BodyFrame)
        if (surveyLoc):
            self.survey = UmatiSurveyTaskWidget.SurveyTaskGui(surveyLoc, method="linear", parent=self.ui.BodyFrame)
        else:
            self.survey = None

        self.ui.vendButton.clicked.connect(self.setVendVisible)
        self.ui.resetButton.clicked.connect(self.setChooserVisible)
        self.ui.full_screen.clicked.connect(self.fullScreen)

        #qt ugliness, we keep it here

        self.connect(self, QtCore.SIGNAL('vend_vis'), self.__setVendVisible)
        self.connect(self, QtCore.SIGNAL('chooser_vis'), self.__setChooserVisible)
        self.connect(self, QtCore.SIGNAL('splash_vis'), self.__setSplashVisible)
        self.connect(self, QtCore.SIGNAL('survey_vis'), self.__setSurveyVisible)
        self.connect(self, QtCore.SIGNAL('set_credits'), self.__setCredits)

        self.setSplashVisible()

        WINDOW = self

    def fullScreen(self):
        self.ui.full_screen.hide()
        self.showFullScreen()

    def __setItemVisible(self, item, others):
        item.show()
        for other in others:
            other.hide()

    def setChooserVisible(self):
        self.emit(QtCore.SIGNAL('chooser_vis'))

    def __setChooserVisible(self):
        self.ui.topFrame.show()
        self.ui.resetButton.show()
        self.ui.vendButton.show()
        self.__setItemVisible(self.chooser, [self.vend, self.splash, self.survey])

    def setVendVisible(self):
        self.emit(QtCore.SIGNAL('vend_vis'))

    def __setVendVisible(self):
        self.ui.topFrame.show()
        self.ui.resetButton.show()
        self.ui.vendButton.hide()
        self.__setItemVisible(self.vend, [self.chooser, self.splash, self.survey]) 

    def setSplashVisible(self):
        self.emit(QtCore.SIGNAL('splash_vis'))

    def __setSplashVisible(self):
        self.ui.topFrame.hide()
        self.__setItemVisible(self.splash, [self.vend, self.chooser, self.survey])

    def setSurveyVisible(self):
        self.emit(QtCore.SIGNAL('survey_vis'))

    def __setSurveyVisible(self):
        if (self.survey):
            self.ui.topFrame.show()
            self.ui.resetButton.show()
            self.ui.vendButton.hide()
            self.__setItemVisible(self.survey, [self.chooser, self.splash, self.vend]) 
        else: #if no survey, go to chooser
            self.setChooserVisible()

    def getValue(self):
        return self.ui.lcdNumber.intValue()

    def setCredits(self, creds):
        self.emit(QtCore.SIGNAL('set_credits'), creds)

    def __setCredits(self, creds):
        self.ui.lcdNumber.display(creds)
