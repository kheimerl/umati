from PyQt4 import QtGui, QtCore, uic
import logging

from . import UmatiChooserWidget
from . import UmatiVendWidget
from . import UmatiSplashWidget
from . import UmatiMessageDialog

WINDOW = None

def getMainWindow():
    global WINDOW
    if (WINDOW):
        return WINDOW
    else:
        raise Exception('No Main Window!')

UI_FILE = 'umati/UmatiMainView.ui'

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, conf):
        global WINDOW
        QtGui.QMainWindow.__init__(self)
        self.log = logging.getLogger("umati.UmatiMainWindow.MainWindow")
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)

        #setup other parts
        self.chooser = UmatiChooserWidget.ChooserGui(conf.getElementsByTagName("main_tasks"), 
                                                     parent = self.ui.BodyFrame)
        self.vend = UmatiVendWidget.VendGui(conf.getElementsByTagName("vend_gui"), 
                                            self, parent = self.ui.BodyFrame)
        self.splash = UmatiSplashWidget.SplashGui(conf.getElementsByTagName("splash"), 
                                                  self, parent = self.ui.BodyFrame)
        prelim_tasks = conf.getElementsByTagName("prelim_tasks")
        if (len(prelim_tasks) > 0):
            self.prelim = UmatiChooserWidget.ChooserGui(prelim_tasks, 
                                                        parent = self.ui.BodyFrame)
        else:
            self.prelim = None

        self.ui.vendButton.clicked.connect(self.setVendVisible)
        self.ui.resetButton.clicked.connect(self.setSplashVisible)
        self.ui.taskButton.clicked.connect(self.setChooserVisible)
        self.ui.full_screen.clicked.connect(self.fullScreen)

        #qt ugliness, we keep it here

        self.connect(self, QtCore.SIGNAL('vend_vis'), self.__setVendVisible)
        self.connect(self, QtCore.SIGNAL('chooser_vis'), self.__setChooserVisible)
        self.connect(self, QtCore.SIGNAL('splash_vis'), self.__setSplashVisible)
        self.connect(self, QtCore.SIGNAL('prelim_vis'), self.__setPrelimVisible)
        self.connect(self, QtCore.SIGNAL('set_credits'), self.__setCredits)
        self.connect(self, QtCore.SIGNAL('information'), self.__information)

        self.setSplashVisible()

        WINDOW = self

    def fullScreen(self):
        self.ui.full_screen.hide()
        self.showFullScreen()

    def __setItemVisible(self, item, others):
        for other in others:
            if (other):
                other.hide()
        item.show()

    def setChooserVisible(self):
        self.emit(QtCore.SIGNAL('chooser_vis'))

    def __setChooserVisible(self):
        self.ui.topFrame.show()
        self.ui.taskButton.setChecked(True)
        self.ui.vendButton.setChecked(False)
        self.log.info("Going to chooser view")
        self.__setItemVisible(self.chooser, [self.vend, self.splash, self.prelim])

    def setVendVisible(self):
        self.emit(QtCore.SIGNAL('vend_vis'))

    def __setVendVisible(self):
        self.ui.topFrame.show()
        self.ui.taskButton.setChecked(False)
        self.ui.vendButton.setChecked(True)
        self.log.info("Going to vend view")
        self.__setItemVisible(self.vend, [self.chooser, self.splash, self.prelim]) 

    def setSplashVisible(self):
        self.emit(QtCore.SIGNAL('splash_vis'))

    def __setSplashVisible(self):
        self.ui.topFrame.hide()
        self.log.info("Going to splash view")
        self.__setItemVisible(self.splash, [self.vend, self.chooser, self.prelim])

    def setPrelimVisible(self):
        self.emit(QtCore.SIGNAL('prelim_vis'))

    def __setPrelimVisible(self):
        if (self.prelim):
            self.ui.topFrame.show()
            self.ui.vendButton.setChecked(False)
            self.__setItemVisible(self.prelim, [self.chooser, self.splash, self.vend]) 
        else: #if no prelim tasks, go to chooser
            self.setChooserVisible()

    def setCredits(self, creds):
        self.emit(QtCore.SIGNAL('set_credits'), creds)

    def __setCredits(self, creds):
        self.ui.lcdNumber.display(creds)
        
    def information(self, message):
        self.emit(QtCore.SIGNAL('information'), message)
    
    def __information(self, message):
        UmatiMessageDialog.information(self, message)

    def getValue(self):
        return self.ui.lcdNumber.intValue()
