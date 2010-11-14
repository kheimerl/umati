from PyQt4 import QtGui
import UmatiSurveyView

class SurveyGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatisurveyView.Ui_Form()
        self.ui.setupUi(self)
