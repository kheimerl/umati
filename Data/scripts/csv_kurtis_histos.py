#!/usr/bin/python
import string, sys, getopt
from math import log, exp

opts, args = getopt.getopt(sys.argv[1:], 
                           "c:o:h", ["csv=", "output=", "help"])

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

"""
Let's find out what scores Kurtis
gave to each Student-Question item
"""

kscores = {}
for line in rawlines[1:]:
    spline = line.split(',')
    meth = spline[1]
    if 'urtis' not in meth:
        continue
    stud = string.atoi(spline[3])
    ques = string.atoi(spline[4])
    sq = (stud,ques)
    score = string.atoi(spline[5])
    kscores[sq] = score

"""
Let's see what all our Umati
data looks like, compared to
Kurtis's scores
"""

uraw = {}
mraw = {}
for line in rawlines[1:]:
    spline = line.split(',')
    meth = spline[1]
    stud = string.atoi(spline[3])
    ques = string.atoi(spline[4])
    if ques == 14:  # The 0-10 question
        continue
    sq = (stud,ques)
    score = string.atoi(spline[5])
    kscore = kscores[sq]
    if 'urk' in meth:
        vec = list(mraw.get(kscore, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        mraw[kscore] = list(vec)
    if 'mati' in meth:
        vec = list(uraw.get(kscore, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        uraw[kscore] = list(vec)

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

"""
Let's see what our pruned (two golds)
data looks like for mturk and umati
compared to Kurtis's score
"""

uprune = {}
turk = {}
for line in lines[1:]:
    spline = line.split(',')
    meth = spline[1]
    stud = string.atoi(spline[3])
    ques = string.atoi(spline[4])
    if ques == 14:  # The 0-10 question
        continue
    sq = (stud,ques)
    score = string.atoi(spline[5])
    kscore = kscores[sq]
    if 'mati' in meth:
        vec = list(uprune.get(kscore, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        uprune[kscore] = list(vec)
    if 'urk' in meth:
        vec = list(turk.get(kscore, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        turk[kscore] = list(vec)

outfile.write('KScore\tUmati (All)\t\t\t\t\tMTurk (All)\t\t\t\t\tUmati (Pruned)\t\t\t\t\tMTurk (Pruned)\t\t\t\t\t\n')
outfile.write('\t0\t1\t2\t3\t4\t0\t1\t2\t3\t4\t0\t1\t2\t3\t4\n')
for a in range(5):
    outline = str(a)+'\t'
    vec = list(uraw[a])
    for b in range(5):
        outline = outline + str(round(100*vec[b]/sum(vec))) + '\t'
    vec = list(mraw[a])
    for b in range(5):
        outline = outline + str(round(100*vec[b]/sum(vec))) + '\t'
    vec = list(uprune[a])
    for b in range(5):
        outline = outline + str(round(100*vec[b]/sum(vec))) + '\t'
    vec = list(turk[a])
    for b in range(5):
        outline = outline + str(round(100*vec[b]/sum(vec))) + '\t'
    outfile.write(outline[:-1]+'\n')
outfile.close()

