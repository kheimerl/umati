from PyQt4 import uic, QtGui
import logging, imp, xml.dom.minidom
from functools import partial

from . import UmatiWidget, UmatiMessageDialog, Util

UI_FILE = 'umati/UmatiChooserView.ui'

class ChooserGui(UmatiWidget.Widget):

    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.parent = parent
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.log = logging.getLogger("umati.UmatiChooserWidget.ChooserGui")
        self.tasks = []
        for task_list in conf:
            for task in task_list.getElementsByTagName("task"):
                self.__add_task(task, parent)

    def __add_task(self, task, parent):
        c = task.getAttribute("class")
        mod = __import__("umati." + c, fromlist='').__dict__[c]
        if (task.getAttribute("xml") == ''):
            taskgui = mod.TaskGui(Util.childNode(task), 
                                  parent=parent)
        else:
            taskgui = mod.TaskGui(xml.dom.minidom.parse(
                    task.getAttribute("xml")).documentElement, 
                                  parent=parent)
        taskgui.hide()
        b = QtGui.QPushButton(task.getAttribute("title"))
        #shits super annoying
        x = b.sizePolicy()
        x.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
        b.setSizePolicy(x)
        #again again
        x = b.font()
        x.setPointSize(45)
        b.setFont(x)
        #and that ugliness is done
        
        l = QtGui.QLabel(taskgui.getValue())
        l.setFixedWidth(60)
        x = l.sizePolicy()
        x.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
        l.setSizePolicy(x)
        
        x = l.font()
        x.setPointSize(45)
        l.setFont(x)

        h = QtGui.QHBoxLayout(self)
        h.addWidget(b)
        h.addWidget(l)
                
        b.clicked.connect(partial(self.select_task, len(self.tasks)))
        self.ui.layout.addLayout(h)
        self.tasks.append((taskgui,b,l))

    def select_task(self, task):
        self.hide()
        self.tasks[task][0].show()

    def hide(self):
        self.__hide_tasks()
        UmatiWidget.Widget.hide(self)

    def show(self):
        self.__hide_tasks()
        avail_tasks = []
        for (task, but,l) in self.tasks:
            if(task.available()):
                but.show() #kurtis
                l.show()
                avail_tasks.append(task)
            else:
                but.hide()
        if (len(avail_tasks) > 1):
            UmatiWidget.Widget.show(self)
        elif (len(avail_tasks) == 1):
            self.hide()
            avail_tasks[0].show()
        else:
            UmatiMessageDialog.information(self, "Sorry, there are no more tasks available right now", title="Notice")
            self.parent.parentWidget().parentWidget().setVendVisible()

    def __hide_tasks(self):
        for (t,b,l) in self.tasks:
            t.hide()
            b.hide()
            l.hide()
