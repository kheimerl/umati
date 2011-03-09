from PyQt4 import uic, QtGui, QtCore
import logging, random, re
from functools import partial

from . import UmatiWidget, UmatiTask, UmatiMessageDialog, Util

UI_FILE = 'umati/UmatiGradingTaskView.ui'

class NoQuestionsException(Exception):
    pass

class Question():

    index_re = re.compile("(\s\s\s+)")

    #this guy would load stuff
    def __init__(self, conf):
        self.q = self.__add_newlines(conf.getAttribute("question"))
        self.gold = self.__add_newlines(conf.getAttribute("gold"))
        self.number = conf.getAttribute("number")
        self.maxGrade = int(conf.getAttribute("range"))
        self.cur_img = None
        self.imgs = []
        for img in conf.getElementsByTagName("img"):
            self.imgs.append(img.getAttribute("src"))

    def getNextAnswer(self, answered):
        if (self.available(answered)):
            if (len(self.imgs) > 0):
                self.cur_img = random.choice(self.imgs)
        else:
            self.cur_img = None
        return self.cur_img

    def getCurName(self):
        return self.__genName(self.cur_img)

    def __genName(self, img):
        return (str(self.number) + ":" + img)

    def __add_newlines(self, text):
        return Question.index_re.sub(lambda x: "\n", text)

    #given a set of answered tasks, determines if there are any new questions to be asked
    def available(self, answered):
        for task in answered:
            for img in self.imgs:
                #horribly inefficient
                if task[0] == self.__genName(img):
                    self.imgs.remove(img)
        return (len(self.imgs) > 0)

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
        return self.current_q.getNextAnswer(
            self.controller.get_completed_tasks(self.getType()))

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

    def instructions(self):
        return self.inst

class TaskGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.log = logging.getLogger("umati.UmatiGradingTaskWidget.GradingGui")
        self.__setupTextFields()
        self.conf = conf.getElementsByTagName("grading")[0]
        self.value = conf.getAttribute("value")
        self.mode = conf.getAttribute("mode")
        self.ui.slider.valueChanged.connect(self.__updateGrade)
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
        self.ui.grade.setNum(self.ui.slider.value())

    def __newTask(self):
        self.cur_task = GradingTask(self.conf)
        self.ui.questionField.setText(self.cur_task.getQuestionText())
        self.ui.goldField.setText(self.cur_task.getGoldText())
        self.ui.slider.setRange(0,self.cur_task.getMaxGrade())
        self.__newQuestion()

    def __newQuestion(self):
        ans_loc = self.cur_task.getAnswerLoc()
        if (ans_loc):
            self.__genNewQuestion(ans_loc)
        else:
            self.controller.choose_task()

    def __genNewQuestion(self, ans_loc):
        self.ui.studentField.setUrl(QtCore.QUrl(ans_loc))
        self.ui.slider.setValue(0)
        for field in [self.ui.questionField, self.ui.goldField,
                      self.ui.studentField]:
            field.show()
        for but in [self.ui.questButton, self.ui.profButton,
                    self.ui.studentButton]:
            but.setChecked(False)

    def __submit(self):
        self.log.info("Grading Task COMPLETE. Q: %s A: %d" % 
                      (self.cur_task.getName(), self.ui.slider.value()))
        self.cur_task.setAns(self.ui.slider.value())
        self.controller.task_completed(self.cur_task, reset=False)
        self.__newQuestion()

    def show(self):
        UmatiWidget.Widget.show(self)
        if(self.available()):
            self.__newTask()
            if (len(self.controller.get_completed_tasks(self.cur_task.getType())) == 0):
                UmatiMessageDialog.information(self, self.cur_task.instructions(), title="Intructions")
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
