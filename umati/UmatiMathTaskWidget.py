from PyQt4 import QtGui
import UmatiMathTaskView

class MathTaskGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatiMathTaskView.Ui_Form()
        self.ui.setupUi(self)
