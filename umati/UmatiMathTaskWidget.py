from PyQt4 import QtGui, QtCore, uic
import random

MAX_VAR = 4000

class MathTask:

    def __init__(self, command, answer):
        self.cmd = cmd
        self.ans = answer

    #generate random math question
    def __init__(self):
        #just addition for now
        x = random.randint(0,MAX_VAR)
        y = random.randint(0,MAX_VAR)
        self.cmd = "%d + %d = ?" % (x,y)
        self.ans = x+y

UI_FILE = 'umati/UmatiMathTaskView.ui'

class MathTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.mainWin = mainWin
        
        for i in range(0,10):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            b.val = i
            b.clicked.connect(lambda: self.updateNumber(self.sender().val))

        self.ui.pushButton_submit.clicked.connect(self.send)
        self.ui.pushButton_clear.clicked.connect(self.clear)

        self.generateMathTask()

    def updateNumber(self, b):
        res = self.ui.numberField.intValue()*10 + b
        self.ui.numberField.display(res)

    def clear(self):
        self.ui.numberField.display(0)

    def send(self):
        if (self.ui.numberField.intValue() != 0):
            print ("Supposed to send result now, update task count and stuff")
            self.mainWin.taskCompleted(1)
            self.generateMathTask()
            self.clear()

    def generateMathTask(self):
        self.curTask = MathTask()
        self.ui.questionBox.setText(self.curTask.cmd)
