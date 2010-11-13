#!/usr/bin/python

import sys
from PyQt4 import QtGui
from umati import UmatiMainWindow

app = QtGui.QApplication(sys.argv)
mw = UmatiMainWindow.MainWindow()
mw.show()

sys.exit(app.exec_())
