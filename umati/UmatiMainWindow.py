from PyQt4 import QtGui, QtCore

import UmatiMainView
import UmatiChooserWidget
import UmatiVendWidget
import UmatiMathTaskWidget
import UmatiSurveyTaskWidget

WINDOW = None

def getMainWindow():
    global WINDOW
    if (WINDOW):
        return WINDOW
    else:
        raise Exception('No Main Window!')

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        global WINDOW
        QtGui.QMainWindow.__init__(self)
        self.ui = UmatiMainView.Ui_MainWindow()
        self.ui.setupUi(self)
        
        #setup other parts
        self.chooser = UmatiChooserWidget.ChooserGui(self.ui.BodyFrame)
        self.vend = UmatiVendWidget.VendGui(self.ui.BodyFrame)
        self.math_task = UmatiMathTaskWidget.MathTaskGui(self.ui.BodyFrame)
        self.survey_task = UmatiSurveyTaskWidget.SurveyTaskGui(self.ui.BodyFrame)
        #start with chooser visible
        self.setChooserVisible()
        
        self.ui.vendButton.clicked.connect(self.setVendVisible)
        self.ui.resetButton.clicked.connect(self.setChooserVisible)

        WINDOW = self

    def __setItemVisible(self, item, others):
        item.show()
        for other in others:
            other.hide()

    def setChooserVisible(self):
        self.__setItemVisible(self.chooser, [self.vend, self.math_task,
                                             self.survey_task])

    def setVendVisible(self):
        self.__setItemVisible(self.vend, [self.chooser, self.math_task,
                                          self.survey_task])

    def setMathTaskVisible(self):
        self.__setItemVisible(self.math_task, [self.chooser, self.vend,
                                               self.survey_task])

    def setSurveyTaskVisible(self):
        self.__setItemVisible(self.survey_task, [self.chooser, self.vend,
                                                 self.math_task])
