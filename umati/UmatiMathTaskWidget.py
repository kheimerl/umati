from PyQt4 import QtCore, uic
from . import UmatiMessageDialog, UmatiWidget, UmatiTask
import random, logging

class MathTask(UmatiTask.Task):

    def __init__(self, conf):
        UmatiTask.Task.__init__(self, conf)
        self.value = int(conf.getAttribute("value"))
        self.name = conf.getAttribute("name")
        self.inst = conf.getAttribute("instructions")

    def get_ans(self):
        return str(self.ans)

    def check_res(self):
        raise Exception("Unimplemented")

    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

    def instructions(self):
        return self.inst

class AdditionTask(MathTask):

    MAX_VAR = 4000

    #generate random math question
    def __init__(self, conf):
        MathTask.__init__(self, conf)
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.AdditionTask")
        self.task_type = "Addition_Math_Task"
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

    def getType(self):
        return self.task_type

    def getName(self):
        return MathTask.getName(self) + " " + self.cmd

    def getAns(self):
        return str(self.ans)

class PrimeFactorTask(MathTask):
    
    low_primes = [2,3,5,7]

    MAX_FACTORS = 5

    MAX_VALUE = 999

    ERROR_RANGE = 1

    def __init__(self, conf):
        MathTask.__init__(self, conf)
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.PrimeFactorTask")
        self.task_type = "Prime Factor Task"
        self.ans = []
        res = 1
        for i in range(0,PrimeFactorTask.MAX_FACTORS):
            new = PrimeFactorTask.low_primes[random.randint(0,len(PrimeFactorTask.low_primes)-1)]
            if (res * new > PrimeFactorTask.MAX_VALUE):
                break
            res *= new
            self.ans.append(new)
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

    def getName(self):
        return MathTask.getName(self) + str(self.ans)

    def getType(self):
        return self.task_type

    def getAns(self):
        return str(self.ans)

UI_FILE = 'umati/UmatiMathTaskView.ui'

class TaskGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiMathTaskWidget.MathTaskGui")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.task_conf = conf.getElementsByTagName("math")[0]
        
        for i in range(0,10):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            b.val = i
            b.clicked.connect(lambda: self.updateNumber(self.sender().val))

        self.ui.pushButton_submit.clicked.connect(self.send)
        self.ui.pushButton_clear.clicked.connect(self.clear)

        self.generateMathTask()

    def show(self):
        self.reset()
        UmatiWidget.Widget.show(self)
        if (len(self.controller.get_completed_tasks(self.curTask.getType())) == 0):
            UmatiMessageDialog.information(self, self.curTask.instructions(), title="Intructions")

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
        val = self.curTask.getValue()
        if (res != 0):
            if (self.curTask.check_res(res)):
                self.log.info("Math Task COMPLETE. Q: %s A: %s G: %d V: %d" % 
                              (self.curTask.cmd, self.curTask.get_ans(), 
                               res, val))
                self.controller.task_completed(self.curTask, reset=False)
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
        if (self.task_conf.getAttribute("name") == "Primes"):
            self.curTask = PrimeFactorTask(self.task_conf)
        else:
            self.curTask = AdditionTask(self.task_conf)
        self.ui.questionBox.setText(self.curTask.cmd)
        
    def available(self):
        return True
