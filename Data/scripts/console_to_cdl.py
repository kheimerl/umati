#!/usr/bin/python
import sys, getopt
sys.path.append("..")

opts, args = getopt.getopt(sys.argv[1:], 
                           "o:h", ["help", "output="])

output = None

def usage():
    print ("")
    print ("-h | --help Show this message")
    print ("-o | --output=FILELOC")
    exit(2)

for o,a in opts:
    if o in ("-o", "--output="):
        output = open(a, 'w')
    else:
        usage()

if not (output):
    usage()
    exit(2)

res = []
numwrong = 0
index = 0
method = 'Expert'

print ("Name?")
name = sys.stdin.readline().strip()

output.write("Name,Method,File,Student,Question,Result,Time,Index,Gold_Wrong,Total_Answered,Gender,Age,Education,Relationship,Department,Crowdsourcing_Knowledge,Crowdsourcing_Use\n")

for ex in map(lambda x: str(x), range(7,10)):
    for q in map(lambda x: str(x), range(1,3)):
        print ("Answer to Exam %s Question %s" % (ex, q))
        score = sys.stdin.readline().strip()
        t = "norm"
        hack = '/'
        if (int(ex) == 9):
            t = "gold"
            if (score != "4"):
                numwrong += 1
        if (int(q) >= 10):
            hack = ''
        if (score != ''):
            res.append((hack + ex + "_" + q + ".png:" + t,
                        ex, q, score, str(0.0), str(index)))
            index += 1

for grade in res:
    output.write(name + "," +
                 method + "," +
                 grade[0] + "," +
                 grade[1] + "," +
                 grade[2] + "," +
                 grade[3] + "," +
                 grade[4] + "," +
                 grade[5] + "," +
                 str(numwrong) + "," +
                 str(index) + "," +
                 ",,,,,,\n")
            
