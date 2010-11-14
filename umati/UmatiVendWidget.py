from PyQt4 import QtGui
import UmatiVendView
import Util

class VendGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatiVendView.Ui_Form()
        self.ui.setupUi(self)
