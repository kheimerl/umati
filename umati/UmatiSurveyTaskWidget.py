from PyQt4 import QtGui, uic
import logging

class Question:
    
    def __init__(self, q, opts):
        self.q = q
        self.opts = opts
        self.ans = None

    def set_answer(self, ans):
        self.ans = ans

TASK_VAL = 5

class SurveyTask:

    def __init__(self, questions, survey_type):
        self.qs = questions
        self.type = survey_type

    def __init__(self):
        self.qs = [Question("What color do you like best?",
                    ["Red", "Blue", "Yellow", "Green", "Purple"]),
                   Question("What is your age?",
                    ["0-19", "20-40", "40-60", "60-80", "80+"]),
                   Question("How awesome is this thing?",
                    ["Really Awesome", "Totally Awesome", "Super Sweetly Awesome", "Awesomely Awesome"])]
        self.type = "Basic"

    def num_questions(self):
        return len(self.qs)

    def submit(self):
        return True

UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class SurveyTaskGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiSurveyTaskWidget.SurveyTaskGui")
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
        self.cur_task = SurveyTask()
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
                                  (self.cur_task.type, TASK_VAL))
                    self.mainWin.taskCompleted(TASK_VAL)
                else:
                    self.log.info("Survey Task FAILED. T: %s V: %d" %
                                  (self.cur_task.type, TASK_VAL))

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
