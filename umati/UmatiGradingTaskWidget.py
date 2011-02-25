from PyQt4 import uic, QtGui, QtCore, QtWebKit
import logging, random, time
from functools import partial

from . import UmatiWidget

UI_FILE = 'umati/UmatiGradingTaskView.ui'

class Question():
    
    #this guy would load stuff
    def __init__(self, conf):
        self.q = conf.getAttribute("question")
        self.gold = conf.getAttribute("gold")
        self.number = int(conf.getAttribute("number"))
        self.imgs = []
        for img in conf.getElementsByTagName("img"):
            self.imgs.append(img.getAttribute("src"))

    def getNextAnswer(self):
        if (len(self.imgs) > 1):
            return self.imgs[random.randint(0,len(self.imgs)-1)]
        else:
            return None

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
        self.qs = []
        for q in self.conf.getElementsByTagName("question"):
            self.qs.append(Question(q))
        self.ui.slider.valueChanged.connect(self.__updateGrade)
        self.num_hidden = 0;
        
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

    def __pickQuestion(self):
        #probably an "if random" eventually
        self.current_q = self.qs[random.randint(0,len(self.qs)-1)]
        self.ui.questionField.setText(self.current_q.q)
        self.ui.goldField.setText(self.current_q.gold)
        self.ui.studentField.setUrl(QtCore.QUrl(self.current_q.getNextAnswer()))
        self.ui.slider.setRange(0,self.current_q.number)
        for field in [self.ui.questionField, self.ui.goldField,
                      self.ui.studentField]:
            field.show()
        for but in [self.ui.questButton, self.ui.profButton,
                    self.ui.studentButton]:
            but.setChecked(False)

    def show(self):
        UmatiWidget.Widget.show(self)
        self.__pickQuestion()

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
