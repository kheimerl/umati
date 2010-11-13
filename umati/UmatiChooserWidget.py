from PyQt4 import QtGui
import UmatiChooserView

class ChooserGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatiChooserView.Ui_Form()
        self.ui.setupUi(self)
