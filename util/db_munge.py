#!/usr/bin/python

import sys, pickle
sys.path.append("..")
from umati import UmatiVendDB

from lib2to3.fixes.fix_imports import MAPPING

REVERSE_MAPPING={}
for key,val in MAPPING.items():
    REVERSE_MAPPING[val]=key

print (REVERSE_MAPPING)

class Python_3_Unpickler(pickle.Unpickler):
    """Class for pickling objects from Python 3"""
    def find_class(self,module,name):
        if module in REVERSE_MAPPING:
            module=REVERSE_MAPPING[module]
        __import__(module)
        mod = sys.modules[module]
        klass = getattr(mod, name)
        return klass

def loads(f):
    return Python_3_Unpickler(f).load()  

load = sys.argv[1]

db = loads(open(load, 'rb'))
