#!/usr/bin/python
import string, sys, getopt

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

once = []
twice = []
lines = []
ct = 0
for line in rawlines[1:]:
    ct = ct + 1
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

print len(rawlines), len(lines)

"""
Let's find the posterior distribution of
survey respondent scores for four categories
of response: Umati respondents on Kurtis's answers
(student 9), Umati respondendt on non-Kurtis
answers, and similar for MTurk respondents
"""

"""
Also, here's the (Student, Question) pairs
for which answers were left blank
"""
blanks = [(1,1),
(1,8),
(3,1),
(5,8),
(7,8)]

um_gold = []
um_blank = []
um_non = []
mt_gold = []
mt_blank = []
mt_non = []
for a in range(5):
    um_gold.append(0.5)
    um_non.append(0.5)
    um_blank.append(0.5)
    mt_gold.append(0.5)
    mt_non.append(0.5)
    mt_blank.append(0.5)

for line in lines:
    spline = line.split(',')
    quest = string.atoi(spline[4])
    if quest == 14:
        continue
    score = string.atoi(spline[5])
    student = string.atoi(spline[3])
    meth = spline[1]
    if 'urk' in meth:
        if student == 9:
            mt_gold[score] = mt_gold[score] + 1
        elif (student, quest) in blanks:
            mt_blank[score] = mt_blank[score] + 1
        else:
            mt_non[score] = mt_non[score] + 1
    else:
        if student == 9:
            um_gold[score] = um_gold[score] + 1
        elif (student, quest) in blanks:
            um_blank[score] = um_blank[score] + 1
        else:
            um_non[score] = um_non[score] + 1

outfile.write('Score\tUmati_Gold\tUmati_Blank\tUmati_Non\tMTurk_Gold\tMTurk_Blank\tMTurk_Non\n')
for a in range(5):
    outline = str(a)+'\t'
    outline = outline + str(um_gold[a]/sum(um_gold))+'\t'
    outline = outline + str(um_blank[a]/sum(um_blank))+'\t'
    outline = outline + str(um_non[a]/sum(um_non))+'\t'
    outline = outline + str(mt_gold[a]/sum(mt_gold))+'\t'
    outline = outline + str(mt_blank[a]/sum(mt_blank))+'\t'
    outline = outline + str(mt_non[a]/sum(mt_non))+'\t'
    outfile.write(outline[:-1]+'\n')
outfile.close()
            
