from PyQt4 import QtGui, QtCore, uic
import logging

from . import UmatiChooserWidget
from . import UmatiVendWidget
from . import UmatiMathTaskWidget
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
    
    def __init__(self):
        global WINDOW
        QtGui.QMainWindow.__init__(self)
        self.log = logging.getLogger("umati.UmatiMainWindow.MainWindow")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        
        #setup other parts
        self.chooser = UmatiChooserWidget.ChooserGui(self, self.ui.BodyFrame)
        self.vend = UmatiVendWidget.VendGui(self, self.ui.BodyFrame)
        self.math_task = UmatiMathTaskWidget.MathTaskGui(self, self.ui.BodyFrame)
        self.survey_task = UmatiSurveyTaskWidget.SurveyTaskGui(self, self.ui.BodyFrame)
        #start with chooser visible
        self.setChooserVisible()
        
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
        self.ui.resetButton.hide()
        self.ui.vendButton.show()
        self.__setItemVisible(self.chooser, [self.vend, self.math_task,
                                             self.survey_task])

    def setVendVisible(self):
        self.ui.resetButton.show()
        self.ui.vendButton.hide()
        self.__setItemVisible(self.vend, [self.chooser, self.math_task,
                                          self.survey_task])

    def setMathTaskVisible(self):
        self.ui.resetButton.show()
        self.ui.vendButton.show()
        self.__setItemVisible(self.math_task, [self.chooser, self.vend,
                                               self.survey_task])

    def setSurveyTaskVisible(self):
        self.ui.resetButton.show()
        self.ui.vendButton.show()
        self.__setItemVisible(self.survey_task, [self.chooser, self.vend,
                                                 self.math_task])

    def vendItem(self, value):
        if (self.ui.lcdNumber.intValue() >= value):
            self.ui.lcdNumber.display(self.ui.lcdNumber.intValue() - value)
            return True
        return False

    def getValue(self):
        return self.ui.lcdNumber.intValue()

    def taskCompleted(self, value):
        self.ui.lcdNumber.display(self.ui.lcdNumber.intValue() + value)
