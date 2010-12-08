#!/usr/bin/python

import sys, re, csv
from pylab import *
import numpy
import numpy.numarray as na
import scipy.stats.morestats

#from the actual file
ans_dict = {1:2,
            6:2,
            15:0}

class Question:

    def __init__(self, id, ans, guess):
        if (ans != -1): #here but not in dict, add it
            if (id not in ans_dict):
                ans_dict[id] = ans
            else:
                assert (ans_dict[id] == ans)
        self.id = id
        self.ans = ans
        self.guess = guess
        if (id in ans_dict and ans == -1): #not here but in dict
            self.ans = ans_dict[id]

    def __repr__(self):
        return str(str(self.id) + " G:" + str(self.guess) + " A:" + str(self.ans))

def letter_to_int(letter):
    if (letter == "A"):
        return 0
    elif(letter == "B"):
        return 1
    elif(letter == "C"):
        return 2
    elif(letter == "D"):
        return 3
    elif(letter == "E"):
        return 4

def parse_turk(turk):
    res = []
    d = csv.DictReader(open(turk), 
                       delimiter='\t', 
                       quotechar='\"')
    for row in d:
        for i in range(0,30):
            if (row["Answer." + str(i)]):
                res.append(Question(i, -1, letter_to_int(row["Answer." + str(i)])))
    return res

def parse_log(log):
    
    res = []
    cs_gre_re = re.compile("T:CSGRE R:\[(\d+) G:(\d) A:(\d), (\d+) G:(\d) A:(\d)\]")
    for line in open(log):
        x = cs_gre_re.search(line)
        if (x):
            res.append(Question(int(x.group(1)), int(x.group(3)), int(x.group(2))))
            res.append(Question(int(x.group(4)), int(x.group(6)), int(x.group(5))))

    return res

#here's where we transform the data as we see fit
def transform(l, question):
    if (question.ans != -1):
        l.append(question.ans == question.guess)
    else:
        print (question)
        
if (len(sys.argv) < 2):
    print ("Provide log first, then 'n' then turk")
else:
    mode = "log"
    turk_res = []
    log_res = []
    for x in sys.argv[1:]:
        if (x == "n"):
            mode = "turk"
        else:
            if (mode == "turk"):
                res_list = parse_turk(x)
                for res in res_list:
                    transform(turk_res, res)
            else:
                res_list = parse_log(x)
                for res in res_list:
                    transform(log_res, res)

    for item in [(turk_res,"Turk"),
                 (log_res, "Log")]:
        print ("Mode:%s Correct:%f Var:%f Total:%d" % (item[1], 
                                                       numpy.mean(item[0]), 
                                                       numpy.var(item[0]),
                                                       len(item[0])))
    print (scipy.stats.morestats.oneway(turk_res, log_res))
