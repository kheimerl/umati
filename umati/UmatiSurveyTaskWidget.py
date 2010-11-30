from PyQt4 import QtGui, uic
import logging, xml.dom.minidom
from . import UmatiMessageDialog

class Question:
    
    def __init__(self, node):
        self.ans = None
        self.q = node.getAttribute("text")
        self.opts = []
        for opt in node.getElementsByTagName("answer"):
            self.opts.append(opt.getAttribute("text"))

    def set_answer(self, ans):
        self.ans = ans

class SurveyTask:

    def __init__(self, head):
        self.value = int(head.getAttribute("value"))
        self.type = head.getAttribute("type")
        self.qs = []
        for q in head.getElementsByTagName("question"):
            self.qs.append(Question(q))
                           
    def num_questions(self):
        return len(self.qs)

    def submit(self):
        return True

UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class SurveyTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, surveyLoc, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.SurveyTaskGui")
        self.surveyLoc = surveyLoc
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.mainWin = mainWin

        #little hack here, we insert a fake radio button
        #to deal with qt not allowing there to be none selected sometimes
        self.fake_radio = QtGui.QRadioButton(self.ui.pushButton_0.parent())
        self.fake_radio.hide()
        
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_next.clicked.connect(self.next)

        self.reset()

    def show(self):
        self.reset()
        UmatiMessageDialog.information(self,"Please only ONE survey per person")
        #QtGui.QMessageBox.information(self, "!!", 
        #                              "Please take the survey ONLY ONCE", 
        #                              QtGui.QMessageBox.Ok)
        QtGui.QWidget.show(self)

    def setButtons(self):
        self.ui.questionBox.setText(self.cur_task.qs[self.cur_index].q)
        self.fake_radio.setChecked(True)
        for i in range(0,5):
            b = self.ui.__getattribute__('pushButton_' + str(i))
            if (i < len(self.cur_task.qs[self.cur_index].opts)):
                b.setText(self.cur_task.qs[self.cur_index].opts[i])
                b.setCheckable(True)
                b.clicked.connect(self.next)
                if (self.cur_task.qs[self.cur_index].ans and
                    self.cur_task.qs[self.cur_index].ans == i):
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
        self.cur_task = SurveyTask(xml.dom.minidom.parse(self.surveyLoc).firstChild)
        self.cur_index = 0
        self.setButtons()
    
    def next(self):
        res = self.getChecked()
        if (res != -1):
            if (self.cur_index < self.cur_task.num_questions() - 1):
                self.set_answer(res)
                self.cur_index += 1
                self.setButtons()
            else:
                if (self.cur_task.submit()):
                    self.log.info("Survey Task COMPLETE. T: %s V: %d" %
                                  (self.cur_task.type, self.cur_task.value))
                    self.mainWin.taskCompleted(self.cur_task.value)
                else:
                    self.log.info("Survey Task FAILED. T: %s V: %d" %
                                  (self.cur_task.type, self.cur_task.value))

                self.reset()
                self.mainWin.setChooserVisible()

    def back(self):
        if (self.cur_index > 0):
            res = self.getChecked()
            self.set_answer(res)
            self.cur_index -= 1
            self.setButtons()
        else:
            self.reset()
            self.mainWin.setChooserVisible()

    def set_answer(self, ans):
         self.cur_task.qs[self.cur_index].set_answer(ans)
