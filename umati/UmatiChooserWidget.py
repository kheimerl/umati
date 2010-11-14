from PyQt4 import QtGui, QtCore
import Util
import UmatiChooserView

class ChooserGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatiChooserView.Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.mathButton.clicked.connect(lambda: Util.getMainWindow(self).setMathTaskVisible())
        self.ui.surveyButton.clicked.connect(lambda: Util.getMainWindow(self).setSurveyTaskVisible())
