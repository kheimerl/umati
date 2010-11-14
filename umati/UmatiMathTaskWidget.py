from PyQt4 import QtGui, QtCore
import UmatiMathTaskView
import Util

class MathTaskGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UmatiMathTaskView.Ui_Form()
        self.ui.setupUi(self)
        
        for i in range(0,10):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            b.val = i
            b.clicked.connect(lambda: self.updateNumber(self.sender().val))

        self.ui.pushButton_submit.clicked.connect(self.send)
        self.ui.pushButton_clear.clicked.connect(self.clear)

    def updateNumber(self, b):
        res = self.ui.numberField.intValue()*10 + b
        self.ui.numberField.display(res)

    def clear(self):
        self.ui.numberField.display(0)

    def send(self):
        print ("Supposed to send result now, update task count and stuff")
        Util.getMainWindow(self).taskCompleted(1)
        self.clear()
