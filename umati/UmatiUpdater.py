from PyQt4.Qt import QThread
from PyQt4 import QtGui
import sys
import time
import logging
#python3 nonsense
try: 
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer

#countdown thread, resets machine when finished
class Countdown(QThread):

    COUNTDOWN = 1 * 60

    def __init__(self, parent, timeout):
        QThread.__init__(self)
        self.daemon = True
        self.done = False
        self.reset_timeout = int(timeout)
        self.reset()
        self.parent = parent

    def run(self):
        while not self.done:
            while (self.tm > 0):
                self.tm -= 1
                time.sleep(1)
            self.parent.timeout()
            self.reset()

    def reset(self):
        self.tm = self.reset_timeout

    def stop(self):
        self.done = True

#catches actions and hands them to the UI
class BasicUpdater(QThread):

    def __init__(self, cont, conf):
        QThread.__init__(self)
        self.done = False
        self.daemon = True
        self.cont = cont
        self.cd = Countdown(self, 
                            conf.getAttribute("timeout"))

    def run(self):
        self.cd.start()

    def timeout(self):
        self.cont.timeout()

    def stop(self):
        self.done = False
        
    def reset_countdown(self):
        self.cd.reset()

class NetworkUpdater(BasicUpdater):
    
    PORT = 9090

    def __init__(self, cont, conf):
        BasicUpdater.__init__(self, cont, conf)
        self.server = SimpleXMLRPCServer(("localhost", NetworkUpdater.PORT))
        self.server.register_function(self.connect)
        
    def run(self):
        BasicUpdater.run(self)
        self.server.serve_forever()
            
    def connect(self, client):
        self.cont.new_connection(client)
        return True

class KeyboardUpdater(BasicUpdater):

    UPDATE_MAX = 0.5
    GRANULARITY = 0.1

    def run(self):
        BasicUpdater.run(self)
        while not (self.done):
            if (self.str != "" and time.time() > self.update_time + KeyboardUpdater.UPDATE_MAX): #.5 seconds since last update
                tmpstr = self.str
                self.str = ""
                self.log.info("Scanned %s" % tmpstr)
                self.cont.new_connection(tmpstr)
            else:
                time.sleep(KeyboardUpdater.UPDATE_MAX)

    def updateStr(self, str):
        #will need locks eventually
        self.str += str
        self.update_time = time.time()

    def __init__(self, cont, conf):
        BasicUpdater.__init__(self, cont, conf)
        self.log = logging.getLogger("umati.UmatiUpdater.KeyboardUpdater")
        self.wid = KeyboardWidget(self)
        self.str = ""
        

class KeyboardWidget(QtGui.QWidget):
    
    def __init__(self, updater):
        QtGui.QWidget.__init__(self)
        self.updater = updater
        self.grabKeyboard() #get all the keyboard events

    def keyPressEvent(self, event):
        self.updater.updateStr(event.text())

def Updater(controller, conf):
    type = conf.getAttribute("type")
    if (type == "Keyboard"):
        return KeyboardUpdater(controller, conf)
    elif(type == "Network"):
        return NetworkUpdater(controller, conf)
    else:
        raise Exception("No associated updater")

#unit tests
if __name__ == '__main__':
    
    import sys
    import getopt
    
    def usage():
        print ("Unit tests, read the file")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "bn:", ["basic", "network="])
    except getopt.GetoptError:
        usage()

    up = None
    command = ""

    for o,a in opts:
        if o in ("-b", "--basic"):
            up = "Basic"
        elif o in ("-n", "--network"):
            up = "Network"
            command = a
        else:
            usage()

    if (up == "Basic"):
        print ("No Tests for Basic")
    elif (up == "Network"):
        try:
            import xmlrpclib as xmlclient
        except ImportError:
            import xmlrpc.client as xmlclient
        s = xmlclient.ServerProxy("http://localhost:" + str(NetworkUpdater.PORT))
        s.connect(command)
        print ("test complete")
