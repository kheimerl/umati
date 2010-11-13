#!/usr/bin/python

import sys
from PyQt4 import QtGui
from umati import UmatiMainView

app = QtGui.QApplication(sys.argv)
mw = QtGui.QMainWindow()
mw.ui = UmatiMainView.Ui_MainWindow()
mw.ui.setupUi(mw)

mw.show()
sys.exit(app.exec_())
