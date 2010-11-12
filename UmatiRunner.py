import sys
from PyQt4 import QtGui
from umati import FrontendView

app = QtGui.QApplication(sys.argv)
main = FrontendView.Frontend()
main.show()
sys.exit(app.exec_())
