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

