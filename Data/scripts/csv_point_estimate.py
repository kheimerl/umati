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

udists = {}
tdists = {}
xdists = {}
for line in rawlines[1:]:
    spline = line.split(',')
    meth = spline[1]
    stud = string.atoi(spline[3])
    ques = string.atoi(spline[4])
    if ques == 14:
        continue
    tup = (stud,ques)
    score = string.atoi(spline[5])
    if 'xpert' in meth:
        vec = xdists.get(tup, [0,0,0,0,0])
        vec[score] = vec[score] + 1
        xdists[tup] = list(vec)
    if 'mati' in meth:
        vec = udists.get(tup, [0,0,0,0,0])
        vec[score] = vec[score] + 1
        udists[tup] = list(vec)
    if 'urk' in meth:
        vec = tdists.get(tup, [0,0,0,0,0])
        vec[score] = vec[score] + 1
        tdists[tup] = list(vec)

# Check we have entries for all SQs by each method
##suks = sorted(udists.keys())
##stks = sorted(tdists.keys())
##sxks = sorted(xdists.keys())
##print len(suks), len(stks), len(sxks)
##for a in range(len(suks)):
##    uk = suks[a]
##    tk = stks[a]
##    xk = sxks[a]
##    if uk != tk or uk != xk or xk != tk:
##        print 'ERROR', uk, tk, xk

# Student, Question, XScore (Median), UScore, TScore
sxks = sorted(xdists.keys())
ult = 0
ueq = 0
ugt = 0
tlt = 0
teq = 0
tgt = 0
for a in range(len(sxks)):
    sq = sxks[a]
    xdist = xdists[sq]
    udist = udists[sq]
    tdist = tdists[sq]
    stud = sq[0]
    ques = sq[1]
    n = 0
    for a in range(5):
        n = n + xdist[a]
        if n > 0.5*sum(xdist):
        #if xdist[a] == max(xdist):
            xscore = a
            break
    n = 0
    for a in range(5):
        n = n + udist[a]
        if n > 0.5*sum(udist):
        #if udist[a] == max(udist):
            uscore = a
            break
    n = 0
    for a in range(5):
        n = n + tdist[a]
        if n > 0.5*sum(tdist):
        #if tdist[a] == max(tdist):
            tscore = a
            break
    outline = str(stud)+'\t'+str(ques)+'\t'+str(xscore)+'\t'+str(uscore)+'\t'+str(tscore)+'\n'
    outfile.write(outline)
    if uscore < xscore:
        ult = ult + 1
    elif uscore == xscore:
        ueq = ueq + 1
    else:
        ugt = ugt + 1
    if tscore < xscore:
        tlt = tlt + 1
    elif tscore == xscore:
        teq = teq + 1
    else:
        tgt = tgt + 1
outfile.close()

print 'Umati LT,EQ,GT', (ult, ueq, ugt)
print 'Turk LT,EQ,GT', (tlt, teq, tgt)
    
    
    
        

