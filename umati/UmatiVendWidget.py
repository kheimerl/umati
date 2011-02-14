from PyQt4 import uic
import logging
from . import Util, UmatiWidget

UI_FILE = 'umati/UmatiVendView.ui'

class VendGui(UmatiWidget.Widget):

    def __init__(self, conf, mainWin, parent=None):
        UmatiWidget.Widget.__init__(self, parent)
        self.log = logging.getLogger("umati.UmatiVendWidget.VendGui")
        self.mainWin = mainWin
        self.ui = uic.loadUiType(UI_FILE)[0]()
        self.ui.setupUi(self)
        self.clear()
        
        #buttons
        for i in (list(map(str, range(1,11))) + ['A', 'B', 'C', 'D', 'E', 'F']):
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
        if (len(self.val) in [2,3]):
            if (self.controller.vendItem(self.val)):
                self.log.info("Vending Item COMPLETED. I: %s" % self.val)
            else:
                self.log.info("Vending Item FAILED. I: %s" % self.val)

            self.clear()
