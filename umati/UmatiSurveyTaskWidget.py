from PyQt4 import QtGui, uic
import logging, xml.dom.minidom, random
from . import UmatiMessageDialog

class Question:
    
    def __init__(self, node):
        self.ans = -1
        self.q = node.getAttribute("text")
        self.right = None
        self.opts = []
        for opt in node.getElementsByTagName("answer"):
            self.opts.append(opt.getAttribute("text"))
            if (opt.getAttribute("correct") == "True"):
                self.right = opt.getAttribute("text")

    def set_answer(self, ans):
        self.ans = ans

    def get_correct(self):
        return self.right

    def __repr__(self):
        return str(self.q + "R:" + str(self.ans))

class RandomSurveyTask:

    finish = 2

    def __init__(self, head):
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.LinearSurveyTask")
        self.value = int(head.getAttribute("value"))
        self.type = head.getAttribute("type")
        self.qs = []
        self.done = []
        self.count = 0
        self.cur = None
        for q in head.getElementsByTagName("question"):
            self.qs.append(Question(q)) 

    def next(self):
        if (self.count >= RandomSurveyTask.finish):
            return None
        self.count += 1
        index = random.randint(0,len(self.qs)-1)
        self.cur = self.qs.pop(index)
        self.done.append(self.cur)
        return self.cur
 
    def prev(self):
        return None

    def submit(self):
        self.log.info("Survey Submission: T:%s R:%s V:%d" % (self.type, str(self.done), self.value))
        return True

    #uses current iteration location
    def set_q_answer(self, ans):
        self.cur.set_answer(ans)

class LinearSurveyTask:

    def __init__(self, head):
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.LinearSurveyTask")
        self.value = int(head.getAttribute("value"))
        self.type = head.getAttribute("type")
        self.index = -1
        self.qs = []
        for q in head.getElementsByTagName("question"):
            self.qs.append(Question(q))
  
    def submit(self):
        self.log.info("Survey Submission: T:%s R:%s V:%d" % (self.type, str(self.qs), self.value))
        return True
    
    def next(self):
        self.index += 1
        if (self.index >= len(self.qs)):
            self.index = len(self.qs)
            return None
        return self.qs[self.index]

    def prev(self):
        self.index -= 1
        if (self.index < 0):
            self.index = -1
            return None
        return self.qs[self.index]

    #uses current iteration location
    def set_q_answer(self, ans):
        self.qs[self.index].set_answer(ans)
        
UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class SurveyTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, surveyLoc, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.SurveyTaskGui")
        self.surveyLoc = surveyLoc
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.mainWin = mainWin

        #little hack here, we insert a fake radio button
        #to deal with qt not allowing there to be none selected sometimes
        self.fake_radio = QtGui.QRadioButton(self.ui.pushButton_0.parent())
        self.fake_radio.hide()
        
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_next.clicked.connect(self.next)

        for i in range(0,5):
            self.ui.__getattribute__('pushButton_' + str(i)).clicked.connect(self.next)

    def show(self):
        self.reset()
        UmatiMessageDialog.information(self,"Please only ONE survey per person")
        QtGui.QWidget.show(self)

    def setButtons(self, q):
        self.ui.questionBox.setText(q.q)
        self.fake_radio.setChecked(True)
        for i in range(0,5):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            if (i < len(q.opts)):
                b.setText(q.opts[i])
                b.setCheckable(True)
                if (q.ans and
                    q.ans == i):
                    b.setChecked(True)
                else:
                    b.setChecked(False)
            else:
                b.setText("")
                b.setCheckable(False)

    def getChecked(self):
        for i in range(0,5):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            if (b.isChecked()):
                return i
        return -1

    def reset(self):
        self.cur_task = RandomSurveyTask(xml.dom.minidom.parse(self.surveyLoc).firstChild)
        self.setButtons(self.cur_task.next())
    
    def next(self):
        res = self.getChecked()
        self.cur_task.set_q_answer(res)
        q = self.cur_task.next()
        if (q): #finished
            self.setButtons(q)
        else:
            if (self.cur_task.submit()):
                self.log.info("Survey Task COMPLETE. T: %s V: %d" %
                              (self.cur_task.type, self.cur_task.value))
                self.mainWin.taskCompleted(self.cur_task.value)
            else:
                self.log.info("Survey Task FAILED. T: %s V: %d" %
                              (self.cur_task.type, self.cur_task.value))
            self.mainWin.setChooserVisible()

    def back(self):
        res = self.getChecked()
        self.cur_task.set_q_answer(res)
        q = self.cur_task.prev()
        if (q):
            self.setButtons(q)
        else: #too far back
            self.mainWin.setChooserVisible()
