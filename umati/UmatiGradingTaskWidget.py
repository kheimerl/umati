from PyQt4 import uic, QtGui, QtCore
import logging, random, xml.dom
from functools import partial

from . import UmatiWidget, UmatiTask, UmatiMessageDialog, Util

UI_FILE = 'umati/UmatiGradingTaskView.ui'

class NoQuestionsException(Exception):
    pass

class Answer():
    
    def __init__(self, src):
        self.src = src
        self.type = "norm"

    def isGold(self):
        return False

class GoldAnswer(Answer):
    
    def __init__(self, src, val):
        Answer.__init__(self, src)
        self.type = "gold"
        self.val = val

    def isGold(self):
        return True;

class Question():

    #this guy would load stuff
    def __init__(self, conf):
        self.q = self.__getSubtext(conf.getElementsByTagName("q")[0])
        self.gold = self.__getSubtext(conf.getElementsByTagName("gold")[0])
        self.number = conf.getAttribute("number")
        self.maxGrade = int(conf.getAttribute("range"))
        self.cur_img = None
        self.imgs = []
        for img in conf.getElementsByTagName("img"):
            self.imgs.append(Answer(img.getAttribute("src")))
        self.golds = []
        for gold in conf.getElementsByTagName("test"):
            self.golds.append(GoldAnswer(gold.getAttribute("src"),
                                         int(gold.getAttribute("val"))))

    def __getSubtext(self, node):
        for n in node.childNodes:
            if (n.nodeType == xml.dom.Node.CDATA_SECTION_NODE):
                return n.data
        return ""

    def getNextAnswer(self, answered):
        if (self.__available(answered, self.golds)):
            self.cur_img = random.choice(self.golds)
        elif (self.__available(answered, self.imgs)):
            self.cur_img = random.choice(self.imgs)
        else:
            self.cur_img = None
        if (self.cur_img):
            return self.cur_img.src
        else:
            return None

    def isGold(self):
        return self.cur_img.isGold()

    def isCorrect(self, ans):
        if (self.isGold()):
            return (self.cur_img.val == ans)
        return True

    def getCurName(self):
        return self.__genName(self.cur_img)

    def __genName(self, img):
        return (str(self.number) + ":" + img.src + ":" + img.type)

    def available(self, answered):
        return self.__available(answered, self.imgs)

    #given a set of answered tasks, determines if there are any new questions to be asked
    def __available(self, answered, targetList):
        for task in answered:
            for img in targetList:
                #horribly inefficient
                if task[0] == self.__genName(img):
                    targetList.remove(img)
        return (len(targetList) > 0)

class GradingTask(UmatiTask.Task):
    
    def __init__(self, conf):
        UmatiTask.Task.__init__(self,conf)
        self.value = int(conf.getAttribute("value"))
        qs = []
        for q in conf.getElementsByTagName("question"):
            qs.append(Question(q))
        self.current_q = self.__pickQuestion(qs)
        if not(self.current_q):
            raise NoQuestionsException()
        self.ans = None
        self.inst = conf.getAttribute("instructions")

    def __pickQuestion(self, qs):
        complete = self.controller.get_completed_tasks(self.getType())
        random.shuffle(qs)
        for q in qs:
            if q.available(complete):
                return q
        #should be at FOR level
        return None

    def setAns(self, ans):
        self.ans = ans

    def getQuestionText(self):
        return self.current_q.q

    def getGoldText(self):
        return self.current_q.gold

    def getAnswerLoc(self):
        return self.current_q.getNextAnswer(self.controller.get_completed_tasks(self.getType()))

    def getMaxGrade(self):
        return self.current_q.maxGrade

    def getType(self):
        return "Grading"

    def getValue(self):
        return self.value

    def getName(self):
        return self.current_q.getCurName()

    def getAns(self):
        return str(self.ans)

    def isGold(self):
        return self.current_q.isGold()

    def isCorrect(self):
        return self.current_q.isCorrect(self.ans)

    def instructions(self):
        return self.inst

class TaskGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.log = logging.getLogger("umati.UmatiGradingTaskWidget.GradingGui")
        self.__setupTextFields()
        self.conf = conf
        self.value = self.conf.getAttribute("value")
        self.mode = self.conf.getAttribute("mode")
        self.ui.scroller.valueChanged.connect(self.__updateGrade)
        self.ui.submit.clicked.connect(self.__submit)
        
    def __setupTextFields(self):
        for (field, but, obj, layout, 
             color_get, color_set) in [("questionField", self.ui.questButton, 
                                        UmatiWidget.PanningTextBrowser(self), self.ui.topLayout, 
                                        QtGui.QColor.red, QtGui.QColor.setRed),
                                       ("goldField", self.ui.profButton, 
                                        UmatiWidget.PanningTextBrowser(self), self.ui.topLayout, 
                                        QtGui.QColor.green, QtGui.QColor.setGreen),
                                       ("studentField", self.ui.studentButton, 
                                        UmatiWidget.PanningWebBrowser(self), self.ui.centerLayout, 
                                        QtGui.QColor.blue, QtGui.QColor.setBlue)]:
            self.ui.__dict__[field] = obj
            for tag in [QtGui.QPalette.Base, QtGui.QPalette.Light]:
                pal = obj.palette()
                col = pal.color(tag)
                color_set(col, color_get(col) - 20)
                pal.setColor(tag, col)
                obj.setPalette(pal)
                if (tag == QtGui.QPalette.Base):
                    but.setStyleSheet(
                        "QPushButton { background-color: %s }" %
                        col.name())
            obj.setMinimumHeight(275)
            x = obj.font()
            x.setPointSize(30)
            obj.setFont(x)
            layout.addWidget(obj)
            but.clicked.connect(partial(self.__switchField, obj, but))
        self.num_hidden = 0;
                
    def __switchField(self, field, button):
        if (field.isHidden()):
            field.show()
            self.num_hidden -= 1
        else:
            if (self.num_hidden != 2):
                field.hide()
                self.num_hidden += 1
            else:
                button.setChecked(False)

    def __updateGrade(self):
        self.ui.grade.setNum(self.ui.scroller.value())

    def __newTask(self):
        self.cur_task = GradingTask(self.conf)
        self.ui.questionField.setText(self.cur_task.getQuestionText())
        self.ui.goldField.setText(self.cur_task.getGoldText())
        self.ui.scroller.setRange(0,self.cur_task.getMaxGrade())
        self.__newQuestion()

    def __newQuestion(self):
        ans_loc = self.cur_task.getAnswerLoc()
        if (ans_loc):
            self.__genNewQuestion(ans_loc)
        else:
            self.controller.choose_task()

    def __getHtml(self, img):
        html = '<html><body><img src="%s"/></body></html>' % (img)
        return html

    def __genNewQuestion(self, ans_loc):
        self.ui.studentField.setHtml(self.__getHtml(ans_loc))
        self.ui.scroller.setValue(0)
        self.__resetFields()
        for but in [self.ui.questButton, self.ui.profButton,
                    self.ui.studentButton]:
            but.setChecked(False)

    def __resetFields(self):
        for field in [self.ui.questionField, self.ui.goldField,
                      self.ui.studentField]:
            field.show()
        self.num_hidden = 0

    def __submit(self):
        self.log.info("Grading Task COMPLETE. Q: %s A: %d" % 
                      (self.cur_task.getName(), self.ui.scroller.value()))
        self.cur_task.setAns(self.ui.scroller.value())
        if(self.controller.task_completed(self.cur_task, reset=False)):
            self.__newQuestion()

    def show(self):
        UmatiWidget.Widget.show(self)
        if(self.available()):
            self.__newTask()
            if (len(self.controller.get_completed_tasks(self.cur_task.getType())) == 0):
                UmatiMessageDialog.information(self, self.cur_task.instructions(), title="Intructions")
            else:
                UmatiMessageDialog.information(self, "New Question", title="Note")
        else:
            #no questions, go back to chooser
            UmatiMessageDialog.information(self, "Sorry, there are no more questions available right now", title="Notice")
            self.controller.choose_task()

    def available(self):
        try:
            self.__newTask()
        except NoQuestionsException:
            return False
        return True

    def getValue(self):
        return str(self.value)
