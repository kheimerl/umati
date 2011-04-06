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

def pval4(x):
    """For a degree-4 chi squared value of x, what's the p-value? Run this and you will know."""
    return exp(-1*float(x)/2)*(1 + float(x)/2)

infile = None
outfile = None

for o,a in opts:
    if o in ("-c", "--csv="):
        infile = open(a, 'rb')
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
Let's find the posterior distribution of
survey respondent scores for four categories
of response: Umati respondents on Kurtis's answers
(student 9), Umati respondendt on non-Kurtis
answers, and similar for MTurk respondents
"""

quests = {}
uquests = {}
mquests = {}
for line in lines:
    spline = line.split(',')
    quest = string.atoi(spline[4])
    if quest == 14: # This question is scored from 0 to 10, so ignore it here
        continue
    meth = spline[1]
    score = string.atoi(spline[5])
    vec = list(quests.get(quest, [0.5,0.5,0.5,0.5,0.5]))
    vec[score] = vec[score] + 1
    quests[quest] = list(vec)
    if 'urk' in meth: 
        vec = list(mquests.get(quest, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        mquests[quest] = list(vec)
    else: 
        vec = list(uquests.get(quest, [0.5,0.5,0.5,0.5,0.5]))
        vec[score] = vec[score] + 1
        uquests[quest] = list(vec)

outfile.write('ALL RESPONDENTS\nQNum\t0\t1\t2\t3\t4\tKL Div.\tP-value\tN\n')
for a in sorted(quests.keys()):
    vec = quests[a]
    outline = str(a)+'\t'
    kl = 0.0
    chi2 = 0.0
    N = sum(vec) - 2.5
    for b in range(5):
        p = float(vec[b])/sum(vec)
        kl = kl + p*log(5*p) + 0.2*log(0.2/p)
        chi2 = chi2 + 5*((vec[b]-.5-0.2*N)**2)/N
        outline = outline+str(p)+'\t'
    outline = outline+str(kl)+'\t'+str(pval4(chi2))+'\t'+str(N)+'\n'
    outfile.write(outline)

outfile.write('UMATI RESPONDENTS\nQNum\t0\t1\t2\t3\t4\tKL Div.\tP-value\tN\n')
for a in sorted(uquests.keys()):
    vec = uquests[a]
    outline = str(a)+'\t'
    kl = 0.0
    chi2 = 0.0
    N = sum(vec)-2.5
    for b in range(5):
        p = float(vec[b])/sum(vec)
        kl = kl + p*log(5*p) + 0.2*log(0.2/p)
        chi2 = chi2 + 5*((vec[b]-.5-0.2*N)**2)/N
        outline = outline+str(p)+'\t'
    outline = outline+str(kl)+'\t'+str(pval4(chi2))+'\t'+str(N)+'\n'
    outfile.write(outline)
    
outfile.write('MTURK RESPONDENTS\nQNum\t0\t1\t2\t3\t4\tKL Div.\tP-value\tN\n')
for a in sorted(mquests.keys()):
    vec = mquests[a]
    outline = str(a)+'\t'
    kl = 0.0
    chi2 = 0.0
    N = sum(vec) - 2.5
    for b in range(5):
        p = float(vec[b])/sum(vec)
        kl = kl + p*log(5*p) + 0.2*log(0.2/p)
        chi2 = chi2 + 5*((vec[b]-.5-0.2*N)**2)/N
        outline = outline+str(p)+'\t'
    outline = outline+str(kl)+'\t'+str(pval4(chi2))+'\t'+str(N)+'\n'
    outfile.write(outline)


    
