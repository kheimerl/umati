#!/usr/bin/python

import string, sys, getopt, re, time
from scipy.stats import stats, morestats
from numpy import *
sys.path.append("../..")
from umati import UmatiUpdater

opts, args = getopt.getopt(sys.argv[1:], 
                           "l:o:t:h", ["l=", "output=", "time=",  "help"])

def usage():
    print ("Log file analysis file")
    print ("-l --log=FILE | shared csv file")
    print ("-o --output=FILE | shared csv file")
    print ("-t, --time=NUMBER | time block DEFAULT=60 minutes")
    print ("-h | --help Show this message")
    exit(2)

infile = None
outfile = sys.stdout
time_dif = 60 * 60 #1 hr

for o,a in opts:
    if o in ("-l", "--log="):
        infile = open(a, 'U')
    elif o in ("-o", "--output="):
        outfile = open(a, 'w')
    elif o in ("-t", "--time="):
        time_dif = int(a) * 60
    else:
        usage()

if not (infile):
    usage()

time_re = re.compile("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
task_completed_re = re.compile(" - INFO - (\w+) Task COMPLETE.")
new_user_re = re.compile("- umati.UmatiUpdater.KeyboardUpdater - INFO - Scanned (.+)")
vended_re = re.compile("- INFO - Vending Item COMPLETED.")

def get_time(line):
    return time.mktime(time.strptime(time_re.match(line).group(0), "%Y-%m-%d %H:%M:%S"))

task_times = []
res = []

for row in infile:
    if(task_completed_re.search(row)):
        task_times.append(get_time(row))

cur_time = task_times[0]
last_time = cur_time
count = 0
outfile.write("Users,Time\n")
for t in task_times:
    if (last_time - t > 0): #time went backwards
        res.append((count, cur_time))
        count = 0
        cur_time = t
    last_time = t
    
    if (t <= cur_time + time_dif):
        count += 1
    else:
        res.append((count, cur_time))
        cur_time += time_dif
        count = 0

for item in res:
    print (item)
    outfile.write(str(item[0]) + "," + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item[1])) + "\n")
