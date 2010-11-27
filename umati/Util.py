import logging

LOG_LOC = "umati.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

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

        

