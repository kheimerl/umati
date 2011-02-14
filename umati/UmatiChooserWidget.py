from PyQt4 import uic, QtGui
import logging, imp
from functools import partial

from . import UmatiWidget

UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.log = logging.getLogger("umati.UmatiChooserWidget.ChooserGui")
        self.tasks = []
        for task_list in conf:
            for task in task_list.getElementsByTagName("task"):
                c = task.getAttribute("class")
                mod = __import__("umati." + c, fromlist='').__dict__[c]
                taskgui = mod.TaskGui(task, parent=parent)
                taskgui.hide()
                b = QtGui.QPushButton(task.getAttribute("name"))
                #shits super annoying
                x = b.sizePolicy()
                x.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
                b.setSizePolicy(x)
                #again again
                x = b.font()
                x.setPointSize(30)
                b.setFont(x)
                #and that ugliness is done
                
                b.clicked.connect(partial(self.select_task, len(self.tasks)))
                self.ui.layout.insertWidget(0, b)
                self.tasks.append(taskgui)

    def select_task(self, task):
        self.hide()
        self.tasks[task].show()

    def hide(self):
        self.__hide_tasks()
        UmatiWidget.Widget.hide(self)

    def show(self):
        self.__hide_tasks()
        if (len(self.tasks) != 1):
            UmatiWidget.Widget.show(self)
        else:
            self.hide()
            self.tasks[0].show()

    def __hide_tasks(self):
        for t in self.tasks:
            t.hide()
