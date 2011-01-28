import threading
import sys
import time
from SimpleXMLRPCServer import SimpleXMLRPCServer

#countdown thread, resets machine when finished
class Countdown(threading.Thread):

    COUNTDOWN = 5 * 60

    def __init__(self, parent):
        threading.Thread.__init__(self)
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
class BasicUpdater(threading.Thread):

    def __init__(self, cont):
        threading.Thread.__init__(self)
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
        import xmlrpclib
        s = xmlrpclib.ServerProxy("http://localhost:" + str(NetworkUpdater.PORT))
        s.connect(command)
        print ("test complete")
