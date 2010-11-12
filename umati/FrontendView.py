from PyQt4 import QtGui

TOUCHSCREEN_X = 480
TOUCHSCREEN_Y = 800

class Frontend(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(TOUCHSCREEN_X,TOUCHSCREEN_Y)
        self.setWindowTitle("Umati")
        
        self.statusBar().showMessage('ready')
