#!/usr/bin/python
import sys, pickle, getopt
sys.path.append("..")
from umati import UmatiVendDB

opts, args = getopt.getopt(sys.argv[1:], 
                           "o:h", ["help", "output="])

path = "VendDB"

def usage():
    print ("Create a VendDB file")
    print ("-h | --help Show this message")
    print ("-o | --output=FILELOC")
    exit(2)

for o,a in opts:
    if o in ("-o", "--output="):
        path = a
    else:
        usage()

db = {}

fivers = ["a", "b", "c", "f"]

tenners = ["d", "e"]

def update(let, num, val):
    loc = let + str(num)
    db[loc] = UmatiVendDB.VendItem("", loc, res)

def getRange(let):
    if (let in fivers):
        return range(1,6)
    elif (let in tenners):
        return range(1,11)
    else:
        raise Exception("FUCKED")

for let in fivers + tenners:
    print ("Set one value for all of row %s?" % let)
    res = sys.stdin.readline()
    if (res.lower().strip() in ["yes", "y"]):
        print ("What value for row %s?" % let)
        res = int(sys.stdin.readline())
        for num in getRange(let):
            update(let, num, res)
    else:
        for num in getRange(let):
            print("Whats the value for %s%d?" % (let, num))
            res = int(sys.stdin.readline())
            update(let, num, res)

p = pickle.Pickler(open(path, 'wb'))
p.dump(db)
