from PyQt4 import uic, QtGui, QtCore, QtWebKit
import logging, random, time
from functools import partial

from . import UmatiWidget, UmatiTask

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
        for (field, but, obj, layout) in [("questionField", self.ui.questButton, 
                                           PanningTextBrowser(self), self.ui.topLayout),
                                          ("goldField", self.ui.profButton, 
                                           PanningTextBrowser(self), self.ui.topLayout),
                                          ("studentField", self.ui.studentButton, 
                                           PanningWebBrowser(self), self.ui.centerLayout)]:
            self.ui.__dict__[field] = obj
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
        self.controller.task_completed(self.cur_task, reset=False)
        self.__newQuestion()

    def show(self):
        UmatiWidget.Widget.show(self)
        self.__newTask()

#utility classes, extending QtStuff

class PanningTextBrowser(QtGui.QTextBrowser):
    
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        self.pressed = None

    def mousePressEvent(self, event):
        self.pressed = (event.x(), event.y())
 
    def mouseMoveEvent(self, event):
        if (self.pressed):
            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()
            if (hbar):
                hbar.setValue(hbar.value() + (self.pressed[0] - event.x()))
            if (vbar):
                vbar.setValue(vbar.value() + (self.pressed[1] - event.y()))
            self.pressed = (event.x(), event.y())
 
    def mouseReleaseEvent(self, event):
        self.pressed = None
 
class PanningWebBrowser(QtWebKit.QWebView):

    DOUBLE_CLICK_TIME = 0.25
    RESET_TIME = 0.5

    def __init__(self, parent=None):
        QtWebKit.QWebView.__init__(self, parent)
        self.pressed = None
        self.press_count = 0 #count number of presses
        self.last_press = 0 #last time we completed a press event
        self.press_time = 0 #last time we pressed down
        self.page().mainFrame().setZoomFactor(2.0)
        self.zoomed = True

    def mousePressEvent(self, event):
        self.pressed = (event.x(), event.y())
        self.press_time = time.time()
        if (self.press_time - self.last_press > PanningWebBrowser.RESET_TIME):
            self.press_count = 0

    def mouseMoveEvent(self, event):
        if (self.pressed):
            frame = self.page().mainFrame()
            if (frame):
                cur_pos = frame.scrollPosition()
                frame.setScrollPosition(QtCore.QPoint(
                        cur_pos.x() + self.pressed[0] - event.x(),
                        cur_pos.y() + self.pressed[1] - event.y()))
            self.pressed = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.pressed = None
        if (time.time() - self.press_time < PanningWebBrowser.DOUBLE_CLICK_TIME):
            self.press_count += 1
            self.last_press = time.time()
        if (self.press_count == 2):
            self.press_count = 0
            if (self.zoomed):
                self.page().mainFrame().setZoomFactor(1.0)
                self.zoomed = False
            else:
                self.page().mainFrame().setZoomFactor(2.0)
                self.zoomed = True
