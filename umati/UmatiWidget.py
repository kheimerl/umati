from PyQt4 import QtGui, QtCore, uic, QtWebKit
from . import Util
import time

class Widget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.controller = Util.getUmatiController()
        self.setMouseTracking(True)        
        
    def show(self):
        self.controller.reset_countdown()
        return QtGui.QWidget.show(self)

    def event(self, event):
        self.controller.reset_countdown()
        return QtGui.QWidget.event(self, event)
        
#utility classes, extending QtStuff

class PanningTextBrowser(QtGui.QTextBrowser):
    
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        self.pressed = None

    def mousePressEvent(self, event):
        self.pressed = (event.x(), event.y())
 
    def mouseMoveEvent(self, event):
        if (self.pressed):
            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()
            if (hbar):
                hbar.setValue(hbar.value() + (self.pressed[0] - event.x()))
            if (vbar):
                vbar.setValue(vbar.value() + (self.pressed[1] - event.y()))
            self.pressed = (event.x(), event.y())
 
    def mouseReleaseEvent(self, event):
        self.pressed = None

    def show(self):
        QtGui.QTextBrowser.show(self)
        for bar in [self.horizontalScrollBar(),
                    self.verticalScrollBar()]:
            if (bar):
                bar.hide()

class PanningWebBrowser(QtWebKit.QWebView):

    DOUBLE_CLICK_TIME = 0.25
    RESET_TIME = 0.5

    def __init__(self, parent=None):
        QtWebKit.QWebView.__init__(self, parent)
        self.pressed = None
        self.press_count = 0 #count number of presses
        self.last_press = 0 #last time we completed a press event
        self.press_time = 0 #last time we pressed down
        self.page().mainFrame().setZoomFactor(1.0)
        self.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, 
                                                   QtCore.Qt.ScrollBarAlwaysOff)
        self.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, 
                                                   QtCore.Qt.ScrollBarAlwaysOff)
        self.zoomed = False

    def mousePressEvent(self, event):
        self.pressed = (event.x(), event.y())
        self.press_time = time.time()
        if (self.press_time - self.last_press > PanningWebBrowser.RESET_TIME):
            self.press_count = 0

    def mouseMoveEvent(self, event):
        if (self.pressed):
            frame = self.page().mainFrame()
            if (frame):
                cur_pos = frame.scrollPosition()
                frame.setScrollPosition(QtCore.QPoint(
                        cur_pos.x() + self.pressed[0] - event.x(),
                        cur_pos.y() + self.pressed[1] - event.y()))
            self.pressed = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.pressed = None
        if (time.time() - self.press_time < PanningWebBrowser.DOUBLE_CLICK_TIME):
            self.press_count += 1
            self.last_press = time.time()
        if (self.press_count == 2):
            self.press_count = 0
            if (self.zoomed):
                self.page().mainFrame().setZoomFactor(1.0)
                self.zoomed = False
            else:
                frame = self.page().mainFrame()
                frame.setZoomFactor(2.0)
                frame_size = frame.geometry()
                frame.setScrollPosition(QtCore.QPoint(
                        int((float(event.x())/frame_size.width()) * 
                            frame_size.width()),
                        int((float(event.y())/frame_size.height()) * 
                            frame_size.height())))
                self.zoomed = True
