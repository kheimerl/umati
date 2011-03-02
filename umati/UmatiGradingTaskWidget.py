from PyQt4 import uic, QtGui, QtCore
import logging, random, time
from functools import partial

from . import UmatiWidget, UmatiTask, UmatiMessageDialog

UI_FILE = 'umati/UmatiGradingTaskView.ui'

class Question():
    
    #this guy would load stuff
    def __init__(self, conf):
        self.q = conf.getAttribute("question")
        self.gold = conf.getAttribute("gold")
        self.number = int(conf.getAttribute("number"))
        self.maxGrade = int(conf.getAttribute("range"))
        self.imgs = []
        for img in conf.getElementsByTagName("img"):
            self.imgs.append(img.getAttribute("src"))

    def getNextAnswer(self):
        if (len(self.imgs) > 1):
            return self.imgs[random.randint(0,len(self.imgs)-1)]
        else:
            return None

class GradingTask(UmatiTask.Task):
    
    def __init__(self, conf):
        UmatiTask.Task.__init__(self,conf)
        self.value = int(conf.getAttribute("value"))
        qs = []
        for q in conf.getElementsByTagName("question"):
            qs.append(Question(q))
        self.current_q = qs[random.randint(0,len(qs)-1)]
        self.cur_img = None
        self.ans = None

    def setAns(self, ans):
        self.ans = ans

    def getQuestionText(self):
        return self.current_q.q

    def getGoldText(self):
        return self.current_q.gold

    def getAnswerLoc(self):
        self.cur_img = self.current_q.getNextAnswer()
        return self.cur_img

    def getMaxGrade(self):
        return self.current_q.maxGrade

    def getType(self):
        return "Grading"

    def getValue(self):
        return self.value

    def getName(self):
        return str(self.current_q.number) + ":" + self.cur_img

    def getAns(self):
        return str(self.ans)

    def instructions(self):
        return "Test"

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
        self.ui.studentField.setUrl(QtCore.QUrl(self.cur_task.getAnswerLoc()))
        self.ui.slider.setValue(0)
        for field in [self.ui.questionField, self.ui.goldField,
                      self.ui.studentField]:
            field.show()
        for but in [self.ui.questButton, self.ui.profButton,
                    self.ui.studentButton]:
            but.setChecked(False)

    def __submit(self):
        self.log.info("Grading Task COMPLETE. Q: %s A: %d" % (self.cur_task.getName(), self.ui.slider.value()))
        self.cur_task.setAns(self.ui.slider.value())
        self.controller.task_completed(self.cur_task, reset=False)
        self.__newQuestion()

    def show(self):
        UmatiWidget.Widget.show(self)
        self.__newTask()
        if (len(self.controller.get_completed_tasks(self.cur_task.getType())) == 0):
            UmatiMessageDialog.information(self, self.cur_task.instructions())

