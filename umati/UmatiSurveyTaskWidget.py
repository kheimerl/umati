from PyQt4 import QtGui, uic
import Util

class Question:
    
    def __init__(self, q, opts):
        self.q = q
        self.opts = opts

    def set_answer(self, ans):
        self.ans = ans

class SurveyTask:

    def __init__(self, questions):
        self.qs = questions

    def __init__(self):
        self.qs = [Question("What color do you like best?",
                    ["Red", "Blue", "Yellow", "Green", "Purple"]),
                   Question("What is your age?",
                    ["0-19", "20-40", "40-60", "60-80", "80+"]),
                   Question("How awesome is this thing?",
                    ["Really Awesome", "Totally Awesome", "Super Sweetly Awesome", "Awesomely Awesome"])]

    def num_questions(self):
        return len(self.qs)

    def submit(self):
        pass

UI_FILE = 'umati/UmatiSurveyTaskView.ui'

class SurveyTaskGui(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)

        #little hack here, we insert a fake radio button
        #to deal with qt not allowing there to be none selected sometimes
        self.fake_radio = QtGui.QRadioButton(self.ui.radioButton_0.parent())
        self.fake_radio.hide()
        
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_next.clicked.connect(self.next)

        self.reset()

    def setButtons(self):
        self.ui.questionBox.setText(self.cur_task.qs[self.cur_index].q)
        self.fake_radio.setChecked(True)
        for i in range(0,5):
            b = self.ui.__getattribute__('radioButton_' + str(i))
            if (i < len(self.cur_task.qs[self.cur_index].opts)):
                b.setText(self.cur_task.qs[self.cur_index].opts[i])
                b.setCheckable(True)
            else:
                b.setText("")
                b.setCheckable(False)

    def getChecked(self):
        for i in range(0,5):
            b = self.ui.__getattribute__('radioButton_' + str(i))
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
                self.cur_task.qs[self.cur_index].set_answer(res)
                self.cur_index += 1
                self.setButtons()
            else:
                self.cur_task.submit()
                self.reset()
                mw = Util.getMainWindow(self)
                mw.taskCompleted(5)
                mw.setChooserVisible()

    def back(self):
        if (self.cur_index > 0):
            self.cur_index -= 1
            self.setButtons()
            ans = self.cur_task.qs[self.cur_index].ans
            b = self.ui.__getattribute__('radioButton_' + str(ans))
            b.setChecked(True)
