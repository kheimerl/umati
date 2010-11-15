from PyQt4 import QtGui, QtCore, uic
import Util

UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        
        self.ui.mathButton.clicked.connect(lambda: Util.getMainWindow(self).setMathTaskVisible())
        self.ui.surveyButton.clicked.connect(lambda: Util.getMainWindow(self).setSurveyTaskVisible())
