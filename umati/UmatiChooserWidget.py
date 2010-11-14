from PyQt4 import QtGui, QtCore
import Util
import UmatiChooserView

class ChooserGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        print(parent.parent().parent())
        self.ui = UmatiChooserView.Ui_Form()
        self.ui.setupUi(self)
        
        QtCore.QObject.connect(self.ui.mathButton, QtCore.SIGNAL('clicked()'),
                               lambda: Util.getMainWindow(self).setMathTaskVisible())
        QtCore.QObject.connect(self.ui.surveyButton, QtCore.SIGNAL('clicked()'),
                               lambda: Util.getMainWindow(self).setSurveyTaskVisible())
