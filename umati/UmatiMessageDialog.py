from PyQt4 import QtGui, uic
import logging
from . import UmatiWidget

UI_FILE = 'umati/UmatiMessageView.ui'

def information(parent, message, title=""):
    if (message and message != ""):
        MessageBox(parent, message, title).show()

class MessageBox(QtGui.QDialog):

    def __init__(self, parent, message, title):
        QtGui.QDialog.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiMessageDialog.MessageBox")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.textBox = UmatiWidget.PanningTextBrowser(self)
        self.ui.textBox.setText(message)
        self.ui.gridLayout.addWidget(self.ui.textBox,0,0)
        self.ui.ok.clicked.connect(self.ok)

    def ok(self):
        self.accept()
