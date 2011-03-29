#!/usr/bin/python

import sys, pickle
sys.path.append("..")
from umati import UmatiVendDB

load = sys.argv[1]
dump = sys.argv[2]

p_l = pickle.Unpickler(open(load, 'rb'))
p_d = pickle.Pickler(open(dump, 'wb'), protocol=2)
db = p_l.load()
p_d.dump(db)
