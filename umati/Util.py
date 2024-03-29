import logging
import serial

LOG_LOC = "umati.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

SERIAL_LOC = 'COM3'
SERIAL_BR = 9600

ser = None
try: 
    ser = serial.Serial(SERIAL_LOC, SERIAL_BR)
except serial.serialutil.SerialException:
    print ("Serial port failed to open")

def getLogLevel(log_level):
    if (log_level == "DEBUG"):
        return logging.DEBUG
    elif(log_level == "INFO"):
        return logging.INFO
    elif(log_level == "WARNING"):
        return logging.WARNING
    elif(log_level == "ERROR"):
        return logging.ERROR
    elif(log_level == "CRITICAL"):
        return logging.CRITICAL
    else:
        return None

def sendVendCmd(cmd):
    global ser
    if (ser):
        if (len(cmd) == 2):
            cmd = cmd[0] + '0' + cmd[1]
        cmd = cmd.lower().encode('ascii')
        ser.write(cmd)

control = None

#this is an unenforced singleton
def getUmatiController():
    global control
    return control

def setUmatiController(controller):
    global control
    control = controller

def get_tag(conf, tag):
    x = conf.getElementsByTagName(tag)
    if (not x or len(x) != 1):
        raise Exception("Bad XML for tag:%s" % tag)
    else:
        return x[0]

def childNode(conf):
    node = conf.firstChild
    while (node.nodeType == node.TEXT_NODE):
        node = node.nextSibling
    return node
