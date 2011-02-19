from PyQt4 import QtGui, uic
from . import UmatiWidget
import logging

UI_FILE = 'umati/UmatiSplashView.ui'

class SplashGui(UmatiWidget.Widget):

    def __init__(self, conf, mainWin, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSplashWidget.SplashGui")
        self.mainWin = mainWin
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        if (len(conf) == 1):
            self.ui.splash.setText(conf[0].getAttribute("text"))
