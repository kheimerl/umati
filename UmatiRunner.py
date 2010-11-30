#!/usr/bin/python

import sys
import logging
import getopt
from PyQt4 import QtGui
from umati import UmatiMainWindow, Util

opts, args = getopt.getopt(sys.argv[1:], 
                           "l:s:h", ["help", "logLevel=", "survey="])

def usage():
    print ("The Umati Vending Machine User Interface")
    print ("-h | --help Show this message")
    print ("-l LOGLEVEL | --logLevel=[DEBUG|INFO|WARNING|ERROR|CRITICAL] Default is INFO")
    print ("-s LOC | --survey=LOC")
    exit(2)

log_level = "INFO"
survey_conf = "conf/survey.xml"

for o,a in opts:
    if o in ("-l", "--logLevel="):
        log_level = a
    elif o in ("-s", "--survey="):
        survey_conf = a
    else:
        usage()

log_level = Util.getLogLevel(log_level)
if not (log_level):
    print ("Invalid Log Level")
    usage()

logging.basicConfig(filename=Util.LOG_LOC, 
                    level=log_level, 
                    format=Util.LOG_FORMAT)

app = QtGui.QApplication(sys.argv)
mw = UmatiMainWindow.MainWindow(surveyLoc = survey_conf)
mw.show()

sys.exit(app.exec_())
