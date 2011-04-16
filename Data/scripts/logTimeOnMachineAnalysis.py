#!/usr/bin/python

import string, sys, getopt, re, time
from scipy.stats import stats, morestats
from numpy import *
sys.path.append("../..")
from umati import UmatiUpdater

opts, args = getopt.getopt(sys.argv[1:], 
                           "l:o:m:h", ["l=", "output=", "minJobs=", "help"])

def usage():
    print ("Munge the converted csv file")
    print ("-l --log=FILE | shared csv file")
    print ("-o --output=FILE | shared csv file")
    print ("-m, --minJobs=NUMBER | minimum jobs completed to count. Default 1")
    print ("-h | --help Show this message")
    exit(2)

infile = None
outfile = sys.stdout
minJobs = 1

for o,a in opts:
    if o in ("-l", "--log="):
        infile = open(a, 'U')
    elif o in ("-o", "--output="):
        outfile = open(a, 'w')
    elif o in ("-m", "--minJobs="):
        minJobs = int(a)
    else:
        usage()

if not (infile):
    usage()

time_re = re.compile("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
task_completed_re = re.compile(" - INFO - (\w+) Task COMPLETE.")
new_user_re = re.compile("- umati.UmatiUpdater.KeyboardUpdater - INFO - Scanned (.+)")
vended_re = re.compile("- INFO - Vending Item COMPLETED.")

class user(object):
    
    def __init__(self, name, start):
        self.name = name
        self.start = start
        self.last = start
        self.count = 0

def get_time(line):
    return time.mktime(time.strptime(time_re.match(line).group(0), "%Y-%m-%d %H:%M:%S"))

res = []
num_tasks = []
def add_user(user):
    global res, minJobs
    if (cur_user and 
        cur_user.name not in ";019582227=1140?" and
        cur_user.count >= minJobs):
        res.append(cur_user.last - cur_user.start)
        num_tasks.append(cur_user.count)

cur_user = None
for row in infile:
    if (new_user_re.search(row)):
        add_user(user)
        cur_user = user(new_user_re.search(row).group(1), get_time(row))
    elif(task_completed_re.search(row)):
        cur_user.count += 1
        cur_user.last = get_time(row)
    elif(vended_re.search(row)):
        cur_user.last = get_time(row)

outfile.write(str((mean(res), median(res), std(res), min(res), max(res))))
outfile.write("\n")
outfile.write(str((mean(num_tasks), median(num_tasks), std(num_tasks), min(num_tasks), max(num_tasks))))
