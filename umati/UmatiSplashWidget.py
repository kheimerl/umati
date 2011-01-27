from PyQt4 import QtGui, uic
import logging

UI_FILE = 'umati/UmatiSplashView.ui'

class SplashGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSplashWidget.SplashGui")
        self.mainWin = mainWin
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
