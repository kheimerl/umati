from PyQt4 import uic, QtGui
import logging, random

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
        self.questionField = QtGui.QTextBrowser(parent=self.ui.mainArea)
        self.goldField = QtGui.QTextBrowser(parent=self.ui.mainArea)    
        self.studentField = QtGui.QTextBrowser(parent=self.ui.mainArea)
        self.ui.mainArea.addSubWindow(self.studentField)
        self.ui.mainArea.addSubWindow(self.goldField)
        self.ui.mainArea.addSubWindow(self.questionField)
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
