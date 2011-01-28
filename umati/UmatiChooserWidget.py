from PyQt4 import uic
import logging

from . import UmatiMathTaskWidget
from . import UmatiSurveyTaskWidget
from . import UmatiWidget


UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.log = logging.getLogger("umati.UmatiChooserWidget.ChooserGui")

        if (conf):
            self.math_task = UmatiSurveyTaskWidget.SurveyTaskGui(conf, parent = parent, method = "random")
        else:
            self.math_task = UmatiMathTaskWidget.MathTaskGui(parent= parent)
        
        self.ui.mathButton.clicked.connect(self.mathVisible)

    def mathVisible(self):
        UmatiWidget.Widget.hide(self)
        self.math_task.show()
        
    def hide(self):
        self.math_task.hide()
        UmatiWidget.Widget.hide(self)

    def show(self):
        self.math_task.hide()
        UmatiWidget.Widget.show(self)

