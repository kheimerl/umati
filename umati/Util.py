try:
    from . import UmatiMainWindow
except ImportError:
    pass

def getMainWindow(widget):
    return umw.getMainWindow()
