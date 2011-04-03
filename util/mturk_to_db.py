#!/usr/bin/python

import csv, sys, getopt, pickle
sys.path.append("..")
from umati import UmatiUserDirectory

opts, args = getopt.getopt(sys.argv[1:], 
                           "o:h", ["output=", "help"])

def usage():
    print ("Convert from mturk output to umati_db")
    print ("./mturk_to_db.py TURK_FILES")
    print ("-o --output=FILE | output file for umati_db")
    print ("-h | --help Show this message")
    exit(2)

output = "umati_db.out"
turk_files = None

for o,a in opts:
    if o in ("-o", "--output="):
        output = a
    else:
        usage()

def munge_turk_out(task_num, out):
    res = []
    start = 1
    if (task_num in [10,11,12,13]):
        start = 4
    for ans in out.split(","):
        if (ans != ""):
            ty = ":norm"
            if (start == 9):
                ty = ":gold"
            res.append(("/%d_%d.png%s" % (start,task_num,ty), ans))
            start += 1
    return res

res = {}
for turk_file in args:
    t = csv.DictReader(open(turk_file, 'rb'))
    for ans in t:
        ID = ans["WorkerId"]
        if ID not in res:
            res[ID] = UmatiUserDirectory.User(ID,0)
            res[ID].tasks_completed["Grading"] = []
        ques = int(ans["Annotation"].split(r"/")[-1][:-3])
        for q in munge_turk_out(ques, ans["Answer 1"]):
            res[ID].tasks_completed["Grading"].append((q[0], q[1], 0.0))
            if (":gold" in q[0]):
                if (ques == 14 and q[1] != "14"):
                    res[ID].gold_wrong +=1 
                elif (ques != 14 and q[1] != "4"):
                    res[ID].gold_wrong += 1

p = pickle.Pickler(open(output, 'wb'))
p.dump(res)
