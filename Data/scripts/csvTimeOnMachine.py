#!/usr/bin/python

import string, sys, getopt, csv
from scipy.stats import stats, morestats
from numpy import *
sys.path.append("../..")
from umati import UmatiUpdater

opts, args = getopt.getopt(sys.argv[1:], 
                           "c:o:h", ["csv=", "output=","help"])

print("Don't use this, it's wrong")

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
cur_user = None
max_wait = 120 #from umati.conf
num_skipped = 0

def store_user(user):
    global res, num_skipped
    if (user):
        if (len(user["Times"]) >= 15):
                res[user["Method"]].append(sum(user["Times"]))
        else:
            num_skipped += 1
        
for row in f:
    if row["Method"] not in res:
        res[row["Method"]] = []

    if (cur_user == None or 
        cur_user["Name"] != row["Name"] or 
        cur_user["Method"] != row["Method"] or
        float(cur_user["Cur_time"]) + max_wait < float(row["Time"])):
        store_user(cur_user)
        cur_user = {"Name" : row["Name"],
                    "Times" : [],
                    "Cur_time" : row["Time"],
                    "Method" : row["Method"]}
    else:
        cur_user["Times"].append(float(row["Time"]) - float(cur_user["Cur_time"]))
        cur_user["Cur_time"] = row["Time"]

outfile.write("Num Skipped:\n")
outfile.write(str(num_skipped) + "\n")
for (method, arr) in res.items():
    outfile.write(method + "\n")
    outfile.write(str((mean(arr), median(arr), std(arr), min(arr), max(arr))) + "\n")
