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
        self.img_loc = "all_Moves.png"

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
        for (field, but) in [(self.ui.questionField, self.ui.questButton),
                             (self.ui.goldField, self.ui.profButton),
                             (self.ui.studentField, self.ui.studentButton)]:
            but.clicked.connect(partial(self.__switchField, field))
                
    def __switchField(self, field):
         if (field.isHidden()):
            field.show()
         else:
            field.hide()

    def __updateGrade(self):
        self.ui.grade.setNum(self.ui.slider.value())

    def __pickQuestion(self):
        #probably an "if random" eventually
        self.current_q = self.qs[random.randint(0,len(self.qs)-1)]
        self.ui.questionField.setText(self.current_q.q)
        self.ui.goldField.setText(self.current_q.gold)
        self.ui.studentField.setPixmap(QtGui.QPixmap(self.current_q.img_loc))
        self.ui.slider.setRange(0,self.current_q.number)

    def show(self):
        UmatiWidget.Widget.show(self)
        self.__pickQuestion()
