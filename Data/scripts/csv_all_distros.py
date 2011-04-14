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
        vec = xdists.get(tup, [0.5, 0.5, 0.5, 0.5, 0.5])
        vec[score] = vec[score] + 1
        xdists[tup] = list(vec)
    if 'mati' in meth:
        vec = udists.get(tup, [0.5, 0.5, 0.5, 0.5, 0.5])
        vec[score] = vec[score] + 1
        udists[tup] = list(vec)
    if 'urk' in meth:
        vec = tdists.get(tup, [0.5, 0.5, 0.5, 0.5, 0.5])
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

# Student, Question, N_x, XDist, N_u, UDist, KL_u, N_t, TDist, KL_t
sxks = sorted(xdists.keys())
for a in range(len(sxks)):
    sq = sxks[a]
    xdist = xdists[sq]
    udist = udists[sq]
    tdist = tdists[sq]
    stud = sq[0]
    ques = sq[1]
    klu = 0
    klt = 0
    uden = sum(udist)
    tden = sum(tdist)
    xden = sum(xdist)
    for a in range(5):
        klu = klu + (udist[a]/uden-xdist[a]/xden)*log((udist[a]/uden)/(xdist[a]/xden))
        klt = klt + (tdist[a]/tden-xdist[a]/xden)*log((tdist[a]/tden)/(xdist[a]/xden))
    outline = str(stud)+'\t'+str(ques)+'\t'+str(xden-2.5)+'\t'
    for a in range(5):
        outline = outline + str(xdist[a]/xden)+'\t'
    outline = outline + str(uden - 2.5) + '\t'
    for a in range(5):
        outline = outline + str(udist[a]/uden)+'\t'
    outline = outline + str(klu)+'\t'
    outline = outline + str(tden - 2.5) + '\t'
    for a in range(5):
        outline = outline + str(tdist[a]/tden)+'\t'
    outline = outline + str(klt)+'\n'
    outfile.write(outline)
outfile.close()
