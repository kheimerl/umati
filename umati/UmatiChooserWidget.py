from PyQt4 import QtGui, QtCore, uic

UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.mainWin = mainWin
        
        self.ui.mathButton.clicked.connect(lambda: self.mainWin.setMathTaskVisible())
        self.ui.surveyButton.clicked.connect(lambda: self.mainWin.setSurveyTaskVisible())
