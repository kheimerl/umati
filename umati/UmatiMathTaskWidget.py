from PyQt4 import QtGui, QtCore, uic
import random, logging

MAX_VAR = 4000
TASK_VAL = 1

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

    def check_res(self, ans):
        #modified hamming distance
        diffs = 0
        #well this is awkward
        for (ch1,ch2) in map(lambda x: (int(x[0]),int(x[1])), 
                             zip(str(ans),str(self.ans))):
            diffs += abs(ch1 - ch2)
        return (diffs < len(str(self.ans)))

UI_FILE = 'umati/UmatiMathTaskView.ui'

class MathTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.MathTaskGui")
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
        res = self.ui.numberField.intValue()
        if (res != 0):
            if (self.curTask.check_res(res)):
                self.log.info("Math Task COMPLETE. Q: %s A: %d G: %d V: %d" % 
                              (self.curTask.cmd, self.curTask.ans, 
                               res, TASK_VAL))
                self.mainWin.taskCompleted(TASK_VAL)
            else:
                self.log.info("Math Task FAILED. Q: %s A: %d G: %d V: %d" % 
                              (self.curTask.cmd, self.curTask.ans, 
                               res, TASK_VAL))
                QtGui.QMessageBox.information(self, "Good Try",
                                              "Answer is clearly incorrect",
                                              QtGui.QMessageBox.Ok)

            self.generateMathTask()
            self.clear()

    def generateMathTask(self):
        self.curTask = MathTask()
        self.ui.questionBox.setText(self.curTask.cmd)
