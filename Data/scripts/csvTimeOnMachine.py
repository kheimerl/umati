#!/usr/bin/python

import string, sys, getopt, csv
from scipy.stats import stats, morestats
from numpy import *
sys.path.append("../..")
from umati import UmatiUpdater

opts, args = getopt.getopt(sys.argv[1:], 
                           "c:o:h", ["csv=", "output=","help"])

def usage():
    print ("Munge the converted csv file")
    print ("-c --csv=FILE | shared csv file")
    print ("-o --output=FILE | shared csv file")
    print ("-h | --help Show this message")
    exit(2)

infile = None
outfile = sys.stdout

for o,a in opts:
    if o in ("-c", "--csv="):
        infile = open(a, 'U')
    elif o in ("-o", "--output="):
        outfile = open(a, 'w')
    else:
        usage()

if not (infile):
    usage()


f = csv.DictReader(infile)
res = {}
cur_time = 0.0
max_wait = UmatiUpdater.Countdown.COUNTDOWN
for row in f:
    if "Method" not in res:
        res["Method"] = []
    
        
