from PyQt4 import QtGui
import UmatiMainView
import UmatiChooserWidget

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = UmatiMainView.Ui_MainWindow()
        self.ui.setupUi(self)
        
        #setup other parts
        self.chooser = UmatiChooserWidget.ChooserGui(self.ui.BodyFrame)
