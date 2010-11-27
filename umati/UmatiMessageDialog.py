from PyQt4 import QtGui, uic
import logging

UI_FILE = 'umati/UmatiMessageView.ui'

def information(parent, message):
    MessageBox(parent, message).show()

class MessageBox(QtGui.QDialog):

    def __init__(self, parent, message):
        QtGui.QDialog.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiMessageDialog.MessageBox")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.ui.textBox.setText(message)
        self.ui.ok.clicked.connect(self.ok)

    def ok(self):
        self.accept()
