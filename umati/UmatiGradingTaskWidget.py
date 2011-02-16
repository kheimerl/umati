from PyQt4 import uic, QtGui, QtCore
import logging, random
from functools import partial

from . import UmatiWidget

UI_FILE = 'umati/UmatiGradingTaskView.ui'

class Question():
    
    #this guy would load stuff
    def __init__(self, conf):
        self.q = conf.getAttribute("question")
        self.gold = conf.getAttribute("gold")
        self.number = int(conf.getAttribute("number"))

    def getNextAnswer(self):
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
        
    def __setupTextFields(self):
        for (field, but) in [("questionField", self.ui.questButton),
                             ("goldField", self.ui.profButton),
                             ("studentField", self.ui.studentButton)]:
            self.__dict__[field] = QtGui.QTextBrowser(parent=self.ui.mainArea)
            window = self.ui.mainArea.addSubWindow(self.__dict__[field])
            window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            but.clicked.connect(partial(self.__switchField, window))
        self.ui.mainArea.tileSubWindows()
                
    def __switchField(self, field):
        if (field.isHidden()):
            field.show()
        else:
            field.hide()
        self.ui.mainArea.tileSubWindows()

    def __updateGrade(self):
        self.ui.grade.setNum(self.ui.slider.value())

    def __pickQuestion(self):
        #probably an "if random" eventually
        self.current_q = self.qs[random.randint(0,len(self.qs)-1)]
        self.questionField.setText(self.current_q.q)
        self.goldField.setText(self.current_q.gold)
        self.ui.slider.setRange(0,self.current_q.number)

    def show(self):
        UmatiWidget.Widget.show(self)
        self.__pickQuestion()
