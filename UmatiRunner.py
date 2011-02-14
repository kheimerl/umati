#!/usr/bin/python

import sys
import logging
import getopt
import xml.dom.minidom
from PyQt4 import QtGui
from umati import UmatiController, Util

opts, args = getopt.getopt(sys.argv[1:], 
                           "l:s:m:h", ["help", "logLevel=", "survey=", "math="])

def usage():
    print ("The Umati Vending Machine User Interface")
    print ("-h | --help Show this message")
    print ("-l LOGLEVEL | --logLevel=[DEBUG|INFO|WARNING|ERROR|CRITICAL] Default is INFO")
    print ("-c CONF | --conf=Conf File location")
    exit(2)

log_level = "INFO"
conf = "conf/umati.xml"

for o,a in opts:
    if o in ("-l", "--logLevel="):
        log_level = a
    elif o in ("-c", "--conf="):
        conf = a
    else:
        usage()

log_level = Util.getLogLevel(log_level)
if not (log_level):
    print ("Invalid Log Level")
    usage()

logging.basicConfig(filename=Util.LOG_LOC, 
                    level=log_level, 
                    format=Util.LOG_FORMAT)

try:
    conf = xml.dom.minidom.parse(conf)
except xml.parsers.expat.ExpatError as e:
    print ("XML File Malformed")
    print (e)
    usage()
    sys.exit(1)

uc = UmatiController.Controller(conf)
uc.start()
