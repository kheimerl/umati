from PyQt4 import QtGui, uic

UI_FILE = 'umati/UmatiVendView.ui'

class VendGui(QtGui.QWidget):

    def __init__(self, mainWin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mainWin = mainWin
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.clear()
        
        #buttons
        for i in (list(map(str, range(1,11))) + ['A', 'B', 'C', 'D', 'E']):
            b = self.ui.__getattribute__('pushButton_' + i)
            b.val = i
            b.clicked.connect(lambda: self.update(self.sender().val))
        
        self.ui.pushButton_clear.clicked.connect(self.clear)
        self.ui.pushButton_vend.clicked.connect(self.vend)
        
    def update(self, val):
        if ((len(self.val) == 0 and val.isupper()) or 
            len(self.val) == 1 and val.isdigit()):
            self.__setNumberFieldDisplay(self.val + val)

    def __setNumberFieldDisplay(self, i):
        self.val = i
        self.ui.numberField.display(self.val)
        
    def clear(self):
        self.__setNumberFieldDisplay("")

    def vend(self):
        if (len(self.val) == 2):
            print ("vend to %s here" % self.val)
            self.mainWin.vendItem(1)
            self.clear()
