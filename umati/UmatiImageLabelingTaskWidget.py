import sys
import pickle
import os
import functools

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
import logging, xml.dom.minidom, random, re
from . import UmatiMessageDialog, UmatiWidget, UmatiTask

class ImageLabelingTask(UmatiTask.Task):

    def __init__(self, head, location):
        UmatiTask.Task.__init__(self, head)
        self.log = logging.getLogger("umati.UmatiImageLabelingTaskWidget.ImageLabelingTask")
        self.images = []
        self.loc = location
        self.value = int(head.getAttribute("value"))
        for f in os.listdir(self.loc):
            #all non txt (tag) files
            if (f[-3:] in ["jpg", "png"]):
                self.images.append(f)
        self.randomize()
	      
    def addTag(self, tag):
        f = open(self.get_tag_file(), 'a')
        f.write (" " + tag)
        f.close()
        
    def getTags(self):
        #if it doesn't exist, we have to create it
        tagFile = self.get_tag_file()
        if (not os.path.exists(tagFile)):
            open(tagFile, 'w').close()
        f = open(tagFile, 'r')
        return f.read()
    
    def randomize(self):
        self.index = random.randint(0, len(self.images)-1)
 
    def next(self):
        self.index += 1
        if (self.index >= len(self.images)):
            self.index = 0

    def prev(self):
        self.index -= 1
        if (self.index < 0):
            self.index = len(self.images) - 1

    def submit(self):
        return True
    
    def get_info(self):
        return None

    def getValue(self):
        return self.value

    def getName(self):
        return None

    def getType(self):
        return "Image_Labeling"

    def getAns(self):
        return "NONE"

    def get_image(self):
        return self.loc + self.images[self.index]

    def get_html(self):
        html = '<html><body><img src="%s"/><p>%s</p></body></html>' % ("file:///"+self.get_image(), self.get_attrib())
        return html

    def get_attrib(self):
        attrib_file = self.get_image()[:-4] + ".txt"
        if (os.path.exists(attrib_file)):
            f = open(attrib_file, 'r')
            return f.read()
        else:
            return ""

    def get_tag_file(self):
        return self.get_image() + ".txt"

    
UI_FILE = 'umati/UmatiImageLabelingTaskView.ui'

class TaskGui(UmatiWidget.Widget):
    
    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiImageLabelingTaskWidget.TaskGui")
        self.conf = conf
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.name = conf.getAttribute("name")
        self.loc = self.conf.getAttribute("location")
        self.cur_task = ImageLabelingTask(self.conf, self.loc)
        self.image_browser = UmatiWidget.PanningWebBrowser(self)
        self.image_browser.setMinimumHeight(320)
        self.image_browser.setMaximumHeight(320)
        self.ui.browser_layout.insertWidget(1,self.image_browser)
        self.ui.previous.clicked.connect(self.prev)
        self.ui.next.clicked.connect(self.next)
        self.setupKeyboard()

    def addText(self):
        text = str(self.ui.inputEdit.text()).strip()
        self.clear()
        if (text not in self.cur_task.getTags().split(" ")):
            self.cur_task.addTag(text)
            if(self.controller.task_completed(self.cur_task, reset=False)):
                self.cur_task.next()
                self.show(False)
        
    def show(self, random=True):
        #print (self.cur_task.get_html())
        #print (self.cur_task.get_attrib())
        if (not self.cur_task.get_image()):
            self.controller.choose_task()
            return
        if (random):
            self.cur_task.randomize()
        #self.image_browser.setUrl(QtCore.QUrl("file:///" + self.cur_task.get_image()))
        self.image_browser.setHtml(self.cur_task.get_html())
        cur_tags = self.cur_task.getTags()
        if (cur_tags != ""):
            self.ui.listEdit.setText("Taboo Words:" + cur_tags)
        else:
            self.ui.listEdit.setText(cur_tags)
        UmatiWidget.Widget.show(self)

    def available(self):
        return (self.cur_task.get_image() != None)

    def getValue(self):
        return str(self.cur_task.getValue())

    def prev(self):
        self.cur_task.prev()
        self.show(False)

    def next(self):
        self.cur_task.next()
        self.show(False)

    def clear(self):
        self.ui.inputEdit.clear()

    def backsp(self):
        if (len(self.ui.inputEdit.text()) > 0):
            self.ui.inputEdit.setText(self.ui.inputEdit.text()[:-1])
            
    def buttonPress(self, button):
        self.ui.inputEdit.setText(self.ui.inputEdit.text() + button)
            
    def setupKeyboard(self):
        #highlevel ones
        self.ui.submit.clicked.connect(self.addText)
        self.ui.clear.clicked.connect(self.clear)
        self.ui.backspace.clicked.connect(self.backsp)
        #and then the whole keyboard
        for key in ['q','w','e','r','t','y','u','i','o','p',
                    'a','s','d','f','g','h','j','k','l','z',
                    'x','c','v','b','n','m']:
            but = self.ui.__getattribute__(key)
            but.clicked.connect(functools.partial(self.buttonPress,key))
