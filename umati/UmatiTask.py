class Task:

    def __init__(self, conf):
        self.prelim = conf.getAttribute("prelim")

    def getValue(self):
        raise Exception("Not Implemented")

    def getName(self):
        raise Exception("Not Implemented")

    def getType(self):
        raise Exception("Not Implemented")
