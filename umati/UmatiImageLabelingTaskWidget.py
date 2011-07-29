import sys
import pickle
import os.path

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
import logging, xml.dom.minidom, random, re
from . import UmatiMessageDialog, UmatiWidget, UmatiTask



class ImageLabelingTask(UmatiTask.Task):

    def __init__(self, head, value):
        UmatiTask.Task.__init__(self, head)
        self.log = logging.getLogger("umati.UmatiImageLabelingTaskWidget.ImageLabelingTask")
        self.value = value
        tagFile=[]
        images = []
        self.image = None
		
			
        for image in head.getElementsByTagName("label"):
            images.append((image.getAttribute("url"), image.getAttribute("tag")))
        #completed = completedTask
        random.shuffle(images)
        
		#shortcut for everythingabove for testing:
        userCompleted = self.controller.get_completed_tasks(self.getType())
        

        temp_set = set()
        for i in userCompleted:
            temp_set.add(i[0])
        for i in images:
            if (i[0] not in temp_set):
                 (self.image, self.tagFile) = i
                 break
	      
    def addTag(self, tag):
        #to do: write tags back to file.
        f=open(self.tagFile,"a")
        f.write(tag + "\n")
        f.close()
        
    def getTags(self):
        # read the file, return the contents
        f = open(self.tagFile,'r')
        tagString = f.read()
        f.close()
        return tagString
 
    def submit(self):
        return True
    
    def get_info(self):
        return None

    def getValue(self):
        return self.value

    def getName(self):
        return self.image

    def getType(self):
        return "Image_Labeling"

    def getAns(self):
        return "NONE"

    def get_image(self):
        return self.image

   
    
UI_FILE = 'umati/UmatiImageLabelingTaskView.ui'

class TaskGui(UmatiWidget.Widget):
    
    def __init__(self, conf, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiImageLabelingTaskWidget.TaskGui")
        self.conf = conf
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.value = int(conf.getAttribute("value"))
        self.name = conf.getAttribute("name")
        self.image_browser = UmatiWidget.PanningWebBrowser(self)
        self.image_browser.setMaximumHeight(250)
        self.ui.mainLayout.insertWidget(0,self.image_browser)
        self.ui.submitButton.clicked.connect(self.addText)
        #self.ui.submitButton.clicked.connect(self.addTag)

    #def addTag(self, tag):
    #    self.tags += tag

    def addText(self):
        text = self.ui.inputEdit.text()
        self.ui.inputEdit.clear()
        if (text not in self.ui.listEdit.toPlainText().split("\n")):
            self.cur_task.addTag(text)
            if(self.controller.task_completed(self.cur_task, reset=False)):
                self.cur_task = ImageLabelingTask(self.conf, self.value)
                self.show()
        
    def show(self):
        if (not self.cur_task.get_image()):
            UmatiMessageDialog.information(self, "You have labeled all the images", title="Notice")
            self.controller.choose_task()
            return
        self.image_browser.setUrl(QtCore.QUrl(self.cur_task.get_image()))
        self.ui.listEdit.setText(self.cur_task.getTags())
        UmatiWidget.Widget.show(self)

    def available(self):
        self.cur_task = ImageLabelingTask(self.conf, self.value)
        return (self.cur_task.get_image() != None)

    def getValue(self):
        return str(self.value)
