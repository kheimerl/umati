from PyQt4.Qt import QThread
from PyQt4 import QtGui
import sys
import time
#python3 nonsense
try: 
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer

#countdown thread, resets machine when finished
class Countdown(QThread):

    COUNTDOWN = 5 * 60

    def __init__(self, parent):
        QThread.__init__(self)
        self.daemon = True
        self.done = False
        self.tm = Countdown.COUNTDOWN
        self.parent = parent

    def run(self):
        while not self.done:
            while (self.tm > 0):
                self.tm -= 1
                time.sleep(1)
            self.parent.timeout()
            self.reset()

    def reset(self):
        self.tm = Countdown.COUNTDOWN

    def stop(self):
        self.done = True

#catches actions and hands them to the UI
class BasicUpdater(QThread):

    def __init__(self, cont):
        QThread.__init__(self)
        self.done = False
        self.daemon = True
        self.cont = cont
        self.cd = Countdown(self)

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

    def __init__(self, cont):
        BasicUpdater.__init__(self, cont)
        self.server = SimpleXMLRPCServer(("localhost", NetworkUpdater.PORT))
        self.server.register_function(self.connect)
        
    def run(self):
        BasicUpdater.run(self)
        self.server.serve_forever()
            
    def connect(self, client):
        self.cont.new_connection(client)
        return True

class KeyboardUpdater(BasicUpdater):
    
    def run(self):
        pass

    def __init__(self, cont):
        BasicUpdater.__init__(self, cont)
        self.wid = KeyboardWidget()

class KeyboardWidget(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.grabKeyboard() #get all the keyboard events

    def keyPressEvent(self, event):
        print (event.type())

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
