#!/usr/bin/python

import sys, pickle, getopt
from db_util import *
from umati import UmatiUserDirectory

opts, args = getopt.getopt(sys.argv[1:], 
                           "u:k:t:e:o:h", ["umati_db=", "kurtis_db=", "turk_db=", "expert_db=", "help"])

umati_db = None
kurtis_db = None
turk_db = None
expert_db = None
output = None

def usage():
    print ("Convert Umati-DBs into CDLs")
    print ("-u --umati_db=FILE | umati_db file location")
    print ("-k --kurtis_db=FILE | kurtis_db file location")
    print ("-t --turk_db=FILE | turk_db file location")
    print ("-e --expert_db=FILE | expert_db file location")
    print ("-o --output=FILE | outputfile")
    print ("-h | --help Show this message")
    exit(2)

for o,a in opts:
    if o in ("-u", "--umati_db="):
        umati_db = normalizeDB(ploads(open(a, 'rb')))
    elif o in ("-k", "--kurtis_db="):
        kurtis_db = normalizeDB(ploads(open(a, 'rb')))
    elif o in ("-t", "--turk_db="):
        turk_db = normalizeDB(ploads(open(a, 'rb')))
    elif o in ("-e", "--expert_db="):
        expert_db = normalizeDB(ploads(open(a, 'rb')))
    elif o in ("-o", "--output="):
        output = a
    else:
        usage()

if not (output):
    usage()
else:
    output = open(output, 'w')

def get_method(db):
    if (db == umati_db):
        return "Umati"
    elif(db == kurtis_db):
        return "Kurtis"
    elif (db == turk_db):
        return "Turk"
    elif (db == expert_db):
        return "Expert"
    else:
        print ("bad db")
        exit(2)

def keep_survey(user):
    return (user.tag != "rr" and
            UmatiUserDirectory.UserDirectory.CAL_ID_RE.match(user.tag))

def get_survey_data(user):
    res = ""
    for func in [get_gender, get_age, get_ed,
                 get_relationship, get_department,
                 get_crowdsourcing_knowledge,
                 get_crowdsourcing_use]:
        if keep_survey(user) and "Linear_Survey" in user.tasks_completed:
            task = user.tasks_completed["Linear_Survey"][0]
            res += func(task[0], task[1])
        if (func != get_crowdsourcing_use):
            res += ","
    return res

#schema
output.write("Name,Method,File,Student,Question,Result,Time,Index,Gold_Wrong,Total_Answered,Gender,Age,Education,Relationship,Department,Crowdsourcing_Knowledge,Crowdsourcing_Use\n")

for db in [umati_db, kurtis_db, turk_db, expert_db]:
    if (db):
        for user in db.values():
            survey = get_survey_data(user)
            if "Grading" in user.tasks_completed:
                i = 0
                for question in user.tasks_completed["Grading"]:
                    try:
                        output.write(user.tag.strip() + "," +
                                     get_method(db) + "," +
                                     question[0] + "," +
                                     question[0][:-9].split("_")[0][-1] + "," +
                                     question[0][:-9].split("_")[1] + "," +
                                     question[1] + "," +
                                     str(question[2]) + "," +
                                     str(i) + "," +
                                     str(user.gold_wrong) + "," +
                                     str(len(user.tasks_completed["Grading"])) + "," +
                                     get_survey_data(user) + "\n")
                        i += 1
                    except:
                        pass
