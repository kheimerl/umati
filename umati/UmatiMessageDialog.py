from PyQt4 import QtGui, uic
import logging
from . import UmatiWidget

UI_FILE = 'umati/UmatiMessageView.ui'

def information(parent, message, title="", fontSize=15):
    if (message and message != ""):
        MessageBox(parent, message, title, fontSize).show()

class MessageBox(QtGui.QDialog):

    def __init__(self, parent, message, title, fontSize):
        QtGui.QDialog.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiMessageDialog.MessageBox")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.textBox = UmatiWidget.PanningTextBrowser(self)
        self.ui.textBox.setText(message)
        self.__setFont(fontSize)
        self.ui.gridLayout.addWidget(self.ui.textBox,0,0)
        self.ui.ok.clicked.connect(self.ok)

    def __setFont(self, fs):
        font = self.ui.textBox.font()
        font.setPointSize(fs)
        self.ui.textBox.setFont(font)

    def ok(self):
        self.accept()
