#!/usr/bin/python

import sys
import logging
import getopt
from PyQt4 import QtGui
from umati import UmatiMainWindow, Util

opts, args = getopt.getopt(sys.argv[1:], 
                           "l:h", ["help", "logLevel="])

def usage():
    print ("The Umati Vending Machine User Interface")
    print ("-h | --help Show this message")
    print ("-l | --logLevel=[DEBUG|INFO|WARNING|ERROR|CRITICAL] Default is INFO")
    exit(2)

log_level = "INFO"

for o,a in opts:
    if (o == "-h" or o == "--help"):
        usage()
    elif o in ("-l", "--logLevel"):
        log_level = a

log_level = Util.getLogLevel(log_level)
if not (log_level):
    print ("Invalid Log Level")
    usage()

logging.basicConfig(filename=Util.LOG_LOC, 
                    level=log_level, 
                    format=Util.LOG_FORMAT)

app = QtGui.QApplication(sys.argv)
mw = UmatiMainWindow.MainWindow()
mw.show()

sys.exit(app.exec_())
