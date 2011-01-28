from PyQt4 import QtGui, QtCore, uic
from . import Util

class Widget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.controller = Util.getUmatiController()
        self.setMouseTracking(True)        
        
    def show(self):
        self.controller.reset_countdown()
        return QtGui.QWidget.show(self)

    def event(self, event):
        self.controller.reset_countdown()
        return QtGui.QWidget.event(self, event)
        
