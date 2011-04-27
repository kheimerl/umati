from PyQt4 import QtGui, uic
import logging, xml.dom.minidom, random, re
from . import UmatiMessageDialog, UmatiWidget, UmatiTask

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

class LinearSurveyTask(UmatiTask.Task):

    def __init__(self, head):
        UmatiTask.Task.__init__(self, head)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.LinearSurveyTask")
        self.value = int(head.getAttribute("value"))
        self.task_name = head.getAttribute("name")
        self.reject = (head.getAttribute("reject") == "True")
        self.index = -1
        self.qs = []
        for q in head.getElementsByTagName("question"):
            self.qs.append(Question(q))
  
    def submit(self):
        self.log.info("Survey Submission: T:%s R:%s V:%d" % (self.getType(), str(self.qs), self.getValue()))
        for q in self.qs:
            if (self.reject and q.ans != q.get_correct()):
                return False
            elif (q.ans == -1):
                return False
        return True
    
    def next(self):
        self.index += 1
        if (self.index > len(self.qs) - 1):
            self.index = len(self.qs) - 1
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
        return None

    def getValue(self):
        return self.value

    def getName(self):
        return self.task_name

    def getType(self):
        return "Linear_Survey"

    def getAns(self):
        res = []
        for q in self.qs:
            res.append(q.ans)
        return str(res)

class RandomSurveyTask(LinearSurveyTask):

    def __init__(self, head):
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.LinearSurveyTask")
        LinearSurveyTask.__init__(self, head)
        self.num = int(head.getAttribute("num"))
        temp_qs = self.qs
        self.qs = []
        for i in range(0,self.num):
            self.qs.append(temp_qs.pop(random.randint(0,len(temp_qs)-1)))

    def get_info(self):
        return None

    def getType(self):
        return "Random_Survey"

    def getName(self):
        temp = []
        for q in self.qs:
            temp.append(q.id)
        temp.sort()
        return LinearSurveyTask.getName(self) + str(temp)

    def getAns(self):
        temp = []
        for q in self.qs:
            temp.append(str(q.id) + " " + str(q.ans))
        return str(temp)
        
UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class TaskGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.TaskGui")
        self.conf = conf
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.ui.questionBox.setReadOnly(True)

        #little hack here, we insert a fake radio button
        #to deal with qt not allowing there to be none selected sometimes
        self.fake_radio = QtGui.QRadioButton(self.ui.pushButton_0.parent())
        self.fake_radio.hide()
        
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_next.clicked.connect(self.next)

        for i in range(0,5):
            self.ui.__getattribute__('pushButton_' + str(i)).clicked.connect(self.next)

        self.reset()

    def show(self):
        self.reset()
        message = self.cur_task.get_info()
        if (message):
            UmatiMessageDialog.information(self, message)
        UmatiWidget.Widget.show(self)

    def setButtons(self, q):
        self.ui.questionBox.clear()
        self.ui.questionBox.insertPlainText(q.q)
        self.fake_radio.setChecked(True)
        for i in range(0,5):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            if (i < len(q.opts)):
                b.setText(q.opts[i])
                b.setCheckable(True)
                if (q.ans == i):
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
        if (self.conf.getAttribute("mode") == "linear"):
            self.cur_task = LinearSurveyTask(self.conf)
        else: #default to this
            self.cur_task = RandomSurveyTask(self.conf)
        self.setButtons(self.cur_task.next())
    
    def next(self):
        res = self.getChecked()
        if (res == -1):
            UmatiMessageDialog.information(self, "Please Complete All Questions!")
            return
        else:
            self.cur_task.set_q_answer(res)
            q = self.cur_task.next()
            if (q): #not finished
                self.setButtons(q)
            else:
                self.log.info("Survey Task COMPLETE. T: %s V:%d N:%s A: %s" %
                              (self.cur_task.getType(), 
                               self.cur_task.getValue(),
                               self.cur_task.getName(),
                               self.cur_task.getAns()))
                if (self.cur_task.submit()):
                    self.controller.task_completed(self.cur_task)
                else:
                    UmatiMessageDialog.information(self, "Incorrect Answer!")

    def back(self):
        res = self.getChecked()
        self.cur_task.set_q_answer(res)
        q = self.cur_task.prev()
        if (q):
            self.setButtons(q)
        else: #too far back
            pass

    def available(self):
        return True

    def getValue(self):
        if (self.cur_task):
            return str(self.cur_task.getValue())
        else:
            return ""
