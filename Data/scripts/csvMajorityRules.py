#!/usr/bin/python
import string, sys, getopt, random
from math import log, exp
from scipy import *
from scipy.stats import stats

opts, args = getopt.getopt(sys.argv[1:], 
                           "c:o:m:M:l:h", ["csv=", "output=", 
                                           "min=", "max=",
                                           "loops=", "help"])

def usage():
    print ("Munge the converted csv file")
    print ("-c --csv=FILE | shared csv file")
    print ("-o --output=FILE | shared csv file")
    print ("-m --min=INT | minimum needed for agreement: default 2")
    print ("-M --max=INT | maximum pulls before giving up: default 10000")
    print ("-l --loops=INT | number of total trials: default 100")
    print ("-h | --help Show this message")
    exit(2)

infile = None
outfile = sys.stdout
MIN_ITERS = 2 # The minumum number of samples for a majority to count
MAX_ITERS = 10000   # The maximum number of samples allowed to find a majority
NUM_MAJORITIES = 100   # The number of time-to-majorities we'd like

for o,a in opts:
    if o in ("-c", "--csv="):
        infile = open(a, 'U')
    elif o in ("-o", "--output="):
        outfile = open(a, 'w')
    elif o in ("-m", "--min="):
        MIN_ITERS = int(a)
    elif o in ("-M", "--max="):
        MAX_ITERS = int(a)
    elif o in ("-l", "--loops="):
        NUM_MAJORITIES = int(a)
    else:
        usage()

if not (infile):
    usage()

rawlines = infile.readlines()
infile.close()

""" Data Format:
0 Name
1 Method
2 File
3 Student
4 Question
5 Result
6 Time
7 Index
8 Gold_Wrong
9 Total_Answered
10 Gender
11 Age
12 Education
13 Relationship
14 Department
15 Crowdsourcing_Knowledge
16 Crowdsourcing_Use
"""

# Find the valid entries
once = []
twice = []
lines = []
for line in rawlines[1:]:
    spline = line.split(',')
    name = spline[0]
    if name in twice:
        continue
    stud = string.atoi(spline[3])
    if stud == 9:
        if name not in once:
            once.append(name)
        else:
            twice.append(name)
    lines.append(line)

# Build the distributions for Umatians
# and Turkers on each (Stud, Ques) pair
uquests = {}
mquests = {}
for line in lines:
    spline = line.split(',')
    quest = string.atoi(spline[4])
    if quest == 14: # This question is scored from 0 to 10, so ignore it here
        continue
    meth = spline[1]
    stud = string.atoi(spline[3])
    score = string.atoi(spline[5])
    pair = (stud,quest)
    if 'urk' in meth: 
        vec = list(mquests.get(pair, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        mquests[pair] = list(vec)
    else: 
        vec = list(uquests.get(pair, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        uquests[pair] = list(vec)

outfile.write('Method(Stud,Ques),Min,Median,Mean,Max,Std\n')

def draw(v):
    den = sum(v)
    r = random.random()
    k = 0
    s = float(v[0])/den
    while s < r:
        k += 1
        s += float(v[k])/den
    return k

def findMajor(dist, lo, hi):
    n = len(dist)
    c = [0 for x in range(n)] #Counts
    it = 0
    while it < hi:
        k = draw(dist)
        c[k] += 1
        if (it >= lo):
            for a in range(n):
                if 2*c[a] > sum(c): # DO we have a majority?
                    return (it, a) #zero indexed
        it += 1
    return (hi, -1)

def print_stuff(majors, res, tag):
    mn = min(majors)
    mx = max(majors)
    avg = mean(majors)
    stddv = std(majors)
    med = median(majors)
    outline = tag +str(pair)+ ',' + str(mn) + ',' + str(med) + ',' + str(avg) + ',' + str(mx) + ',' + str(stddv) + '\n'
    outfile.write(outline)
    #for a in range(NUM_MAJORITIES):
    #    outline = outline + str(majors[a])+','
    #outfile.write(outline[:-1]+'\n')
    if(res):
        outfile.write("Results:" + str(res) + '\n') 

umati_majors = []
mturk_majors = []
for pair in set(uquests.keys() + mquests.keys()):
    for (tag, quests, big_major) in [("Umati:", uquests, umati_majors),
                                     ("MTurk:", mquests, mturk_majors)]:
        if (pair in quests):
            majors = []
            res = [0 for x in range(len(quests[pair]))]
            for a in range(NUM_MAJORITIES):
                (major, i) = findMajor(quests[pair],MIN_ITERS, MAX_ITERS)
                majors.append(major)
                big_major.append(major)
                if (i >= 0):
                    res[i] += 1
            print_stuff(majors, res, tag)

print_stuff(umati_majors, None, "Umati-All:")
print_stuff(mturk_majors, None, "MTurk-All:")
    
outfile.close()
