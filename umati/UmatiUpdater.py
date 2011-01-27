import threading
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer

class BasicUpdater(threading.Thread):

    COUNTDOWN = 5 * 60

    def __init__(self):
        threading.Thread.__init__(self)
        self.done = False
        self.daemon = True

    def run(self):
        raise Error("not implemented")

    def stop(self):
        self.done = False
        
    def reset_countdown(self):
        self.timeleft = BasicUpdater.COUNTDOWN

class NetworkUpdater(BasicUpdater):
    
    PORT = 9090

    def __init__(self):
        BasicUpdater.__init__(self)
        self.server = SimpleXMLRPCServer(("localhost", NetworkUpdater.PORT))
        self.server.register_function(self.connect)
        
    def run(self):
        self.server.serve_forever()
            
    def connect(self, client):
        print (client)
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
