from . import Util

class Task:

    def __init__(self, conf):
        self.controller = Util.getUmatiController()
        self.prelim = conf.getAttribute("prelim")

    def getValue(self):
        raise Exception("Not Implemented")

    def getName(self):
        raise Exception("Not Implemented")

    def getType(self):
        raise Exception("Not Implemented")
    
    def getAns(self):
        raise Exception("Not Implemented")

    def isGold(self):
        return False

    def isCorrect(self):
        return True
    
    def instructions(self):
        return None
