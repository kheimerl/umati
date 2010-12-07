from PyQt4 import QtGui, uic
import logging, xml.dom.minidom, random, re
from . import UmatiMessageDialog

class Question:
    
    index_re = re.compile("(I+\.)")

    word_wrap = 50 #characters
    
    def __init__(self, node):
        self.ans = -1
        self.q = self.__add_newlines(node.getAttribute("text"))
        self.id = node.getAttribute("id")
        self.right = ''
        self.opts = []
        opt_count = 0
        for opt in node.getElementsByTagName("answer"):
            #this is an ungodly fucking hack
            res = opt.getAttribute("text")
            i = Question.word_wrap
            while (True):
                i = res.find(" ", i)
                if (i == -1):
                    break
                else:
                    res = res[:i] + "\n" + res[i:]
                i += Question.word_wrap
            self.opts.append(res)
            if (opt.getAttribute("right") == "T"):
                self.right = opt_count
            opt_count += 1

    def __add_newlines(self, text):
        return Question.index_re.sub(lambda x: "\n" + x.group(1), text)

    def set_answer(self, ans):
        self.ans = ans

    def get_correct(self):
        return self.right

    def __repr__(self):
        return str(self.id + " G:" + str(self.ans) + " A:" + str(self.right))

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
        for q in self.qs:
            if (q.ans == -1):
                return False
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
        if (self.index < len(self.qs)):
            self.qs[self.index].set_answer(ans)

    def get_info(self):
        return "Please only ONE survey per person"

class RandomSurveyTask(LinearSurveyTask):

    finish = 5

    def __init__(self, head):
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.LinearSurveyTask")
        LinearSurveyTask.__init__(self, head)
        temp_qs = self.qs
        self.qs = []
        for i in range(0,RandomSurveyTask.finish):
            self.qs.append(temp_qs.pop(random.randint(0,len(temp_qs)-1)))

    def get_info(self):
        return None
        
UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class SurveyTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, surveyLoc, parent=None, method="linear"):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.SurveyTaskGui")
        self.surveyLoc = surveyLoc
        self.method = method
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.ui.questionBox.setReadOnly(True)
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
        message = self.cur_task.get_info()
        if (message):
            UmatiMessageDialog.information(self, message)
        QtGui.QWidget.show(self)

    def setButtons(self, q):
        self.ui.questionBox.clear()
        self.ui.questionBox.insertPlainText(q.q)
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
        if (self.method == "linear"):
            self.cur_task = LinearSurveyTask(xml.dom.minidom.parse(self.surveyLoc).firstChild)
        if (self.method == "random"):
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
                self.mainWin.setChooserVisible()
            else:
                UmatiMessageDialog.information(self, "Please Complete All Questions!")
                self.back()

    def back(self):
        res = self.getChecked()
        self.cur_task.set_q_answer(res)
        q = self.cur_task.prev()
        if (q):
            self.setButtons(q)
        else: #too far back
            self.mainWin.setChooserVisible()
