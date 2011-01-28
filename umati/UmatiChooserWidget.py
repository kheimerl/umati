from PyQt4 import uic
import logging

from . import UmatiMathTaskWidget
from . import UmatiSurveyTaskWidget
from . import UmatiWidget


UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(UmatiWidget.Widget):

    def __init__(self, mainWin, mathLoc, surveyLoc, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.mainWin = mainWin
        self.log = logging.getLogger("umati.UmatiChooserWidget.ChooserGui")

        if (mathLoc):
            self.math_task = UmatiSurveyTaskWidget.SurveyTaskGui(mathLoc, parent = parent, method = "random")
        else:
            self.math_task = UmatiMathTaskWidget.MathTaskGui(parent= parent)
        if (surveyLoc):
            self.survey_task = UmatiSurveyTaskWidget.SurveyTaskGui(surveyLoc, parent = parent, method="linear")
        else:
            self.survey_task = None
        
        self.ui.mathButton.clicked.connect(self.mathVisible)
        self.ui.surveyButton.clicked.connect(self.surveyVisible)

    def mathVisible(self):
        self.survey_task.hide()
        UmatiWidget.Widget.hide(self)
        self.math_task.show()
        
    def surveyVisible(self):
        self.math_task.hide()
        UmatiWidget.Widget.hide(self)
        self.survey_task.show()

    def hide(self):
        self.math_task.hide()
        self.survey_task.hide()
        UmatiWidget.Widget.hide(self)

    def show(self):
        self.math_task.hide()
        self.survey_task.hide()
        UmatiWidget.Widget.show(self)

