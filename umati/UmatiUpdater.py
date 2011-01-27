import threading
import sys

class Updater(threading.Thread):

    COUNTDOWN = 5 * 60

    def __init__(self):
        threading.Thread.__init__(self)
        self.__done = False
        self.daemon = True

    def run(self):
        while not self.__done:
            pass
            #x = sys.stdin.readline().strip()
            #if (x != ""):
             #   print(x)

    def stop(self):
        self.__done = False
        
    def reset_countdown(self):
        self.timeleft = Updater.COUNTDOWN
