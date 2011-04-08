#!/usr/bin/python
import string, sys, getopt, random
from math import log, exp

opts, args = getopt.getopt(sys.argv[1:], 
                           "c:o:h", ["csv=", "output=", "help"])

def usage():
    print ("Munge the converted csv file")
    print ("-c --csv=FILE | shared csv file")
    print ("-o --output=FILE | shared csv file")
    print ("-h | --help Show this message")
    exit(2)

def draw(v):
    den = sum(v)
    r = random.random()
    k = 0
    s = float(v[0])/den
    while s < r:
        k = k + 1
        s = s + float(v[k])/den
    return k

def findMajor(dist, lo, hi):
    c = [] #Counts
    n = len(dist)
    for a in range(n):
        c.append(0)
    it = 0
    while it < lo:
        it = it + 1
        k = draw(dist)
        c[k] = c[k] + 1
    while it < hi:
        it = it + 1
        k = draw(dist)
        c[k] = c[k] + 1
        for a in range(n):
            if 2*c[a] > sum(c): # DO we have a majority?
                return it
    return hi
        

infile = None
outfile = None

for o,a in opts:
    if o in ("-c", "--csv="):
        infile = open(a, 'U')
    elif o in ("-o", "--output="):
        outfile = open(a, 'w')
    else:
        usage()

if not (infile and outfile):
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

outfile.write('Method(Stud,Ques)\tMin\tMedian\tMean\tMax\tSamples\n')
MIN_ITERS = 5 # The minumum number of samples for a majority to count
MAX_ITERS = 10000   # The maximum number of samples allowed to find a majority
NUM_MAJORITIES = 100   # The number of time-to-majorities we'd like
for pair in uquests.keys():
    majors = []
    for a in range(NUM_MAJORITIES):
        majors.append(findMajor(uquests[pair],MIN_ITERS, MAX_ITERS))
    mn = min(majors)
    mx = max(majors)
    avg = float(sum(majors))/NUM_MAJORITIES
    smaj = sorted(majors)
    med = smaj[NUM_MAJORITIES/2]
    outline = 'Umati'+str(pair) + '\t' + str(mn) + '\t' + str(med) + '\t' + str(avg) + '\t' + str(mx) + '\t'
    for a in range(NUM_MAJORITIES):
        outline = outline + str(majors[a])+'\t'
    outfile.write(outline[:-1]+'\n')
for pair in mquests.keys():
    majors = []
    for a in range(NUM_MAJORITIES):
        majors.append(findMajor(mquests[pair],MIN_ITERS, MAX_ITERS))
    mn = min(majors)
    mx = max(majors)
    avg = float(sum(majors))/NUM_MAJORITIES
    smaj = sorted(majors)
    med = smaj[NUM_MAJORITIES/2]
    outline = 'MTurk'+str(pair)+ '\t' + str(mn) + '\t' + str(med) + '\t' + str(avg) + '\t' + str(mx) +'\t'
    for a in range(NUM_MAJORITIES):
        outline = outline + str(majors[a])+'\t'
    outfile.write(outline[:-1]+'\n')


outfile.close()
    
    

