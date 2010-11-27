from PyQt4 import QtGui, QtCore, uic
from . import UmatiMessageDialog
import random, logging

class MathTask:

    def get_ans(self):
        return str(self.ans)

class AdditionTask(MathTask):

    MAX_VAR = 4000
    TASK_VAL = 1

    #generate random math question
    def __init__(self):
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.AdditionTask")
        #just addition for now
        x = random.randint(0,AdditionTask.MAX_VAR)
        y = random.randint(0,AdditionTask.MAX_VAR)
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

    def get_task_val(self):
        return AdditionTask.TASK_VAL

class PrimeFactorTask(MathTask):
    
    low_primes = [2,3,5,7]

    MAX_FACTORS = 5

    MAX_VALUE = 800

    ERROR_RANGE = 2

    TASK_VAL = 1

    def __init__(self):
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.PrimeFactorTask")
        self.ans = []
        res = 1
        for i in range(0,PrimeFactorTask.MAX_FACTORS):
            new = PrimeFactorTask.low_primes[random.randint(0,len(PrimeFactorTask.low_primes)-1)]
            res *= new
            self.ans.append(new)
            if (res > PrimeFactorTask.MAX_VALUE):
                break
        self.cmd = "Provide all prime factors of %d" % res
        self.ans.sort()

    def check_res(self, ans):
        temp = []
        for i  in list(str(ans)):
            i = int(i)
            if i not in PrimeFactorTask.low_primes:
                self.log.debug("Unprime Given")
                return False
            temp.append(i)
        if (len(temp) > len(self.ans) + PrimeFactorTask.ERROR_RANGE or 
            len(temp) < len(self.ans) - PrimeFactorTask.ERROR_RANGE):
            self.log.debug("Too may or too few primes")
            return False
        return True

    def get_task_val(self):
        return PrimeFactorTask.TASK_VAL

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

    def show(self):
        self.reset()
        QtGui.QWidget.show(self)

    def updateNumber(self, b):
        res = self.ui.numberField.intValue()*10 + b
        self.ui.numberField.display(res)

    def reset(self):
        self.clear()
        self.generateMathTask()

    def clear(self):
        self.ui.numberField.display(0)

    def send(self):
        res = self.ui.numberField.intValue()
        val = self.curTask.get_task_val()
        if (res != 0):
            if (self.curTask.check_res(res)):
                self.log.info("Math Task COMPLETE. Q: %s A: %s G: %d V: %d" % 
                              (self.curTask.cmd, self.curTask.get_ans(), 
                               res, val))
                self.mainWin.taskCompleted(val)
            else:
                self.log.info("Math Task FAILED. Q: %s A: %s G: %d V: %d" % 
                              (self.curTask.cmd, self.curTask.get_ans(),
                               res, val))
                UmatiMessageDialog.information(self,"Answer is clearly incorrect")
                #QtGui.QMessageBox.information(self, "Good Try",
                #                              "Answer is clearly incorrect",
                #                              QtGui.QMessageBox.Ok)
                
            self.reset()

    def generateMathTask(self):
        self.curTask = PrimeFactorTask()
        self.ui.questionBox.setText(self.curTask.cmd)
