#!/usr/bin/python

import sys, getopt
sys.path.append("../..")
from umati import UmatiUserDirectory
from db_util import *

from scipy.stats import stats, morestats
from numpy import *
from functools import partial

opts, args = getopt.getopt(sys.argv[1:], 
                           "u:k:t:e:h", ["umati_db=", "kurtis_db=", "turk_db=", "expert_db="])

umati_db = None
kurtis_db = None
turk_db = None
expert_db = None

def usage():
    print ("Munge Umati-DBs")
    print ("-u --umati_db=FILE | umati_db file location")
    print ("-k --kurtis_db=FILE | kurtis_db file location")
    print ("-t --turk_db=FILE | turk_db file location")
    print ("-e --expert_db=FILE | expert_db file location")
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
    else:
        usage()

all_questions=[]

def munge_per_question(user_db, filter_func = lambda x: True):
    global all_questions
    res = {}
    (num_users, num_qs) = (0,0)
    for user in user_db.values():
        if filter_func(user):
            num_users += 1
            if "Grading" in user.tasks_completed:
                num_qs += len(user.tasks_completed["Grading"])
                for question in user.tasks_completed["Grading"]:
                    if question[0] not in all_questions:
                        all_questions.append(question[0])
                    if question[0] not in res:
                        res[question[0]] = []
                    res[question[0]].append(int(question[1]))
    for tag in res.keys():
        t = array(res[tag])
        res[tag] = (t.mean(), t.std(), stats.stderr(t), 
                    t.var(), t.size)#, morestats.bayes_mvs(t))
    return ((num_users, num_qs), res)

def start():
    ops = []
    res = []
    if (umati_db):
        ops.append((umati_db, remove_kurtis, "Umati-All:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_kurtis, remove_cheaters]), "Umati-NC-All:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["cs_only"], remove_kurtis]), "Umati-CSOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, filters["cs_only"], remove_kurtis]), "Umati-NC-CSOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["ugrad_only"], remove_kurtis]), "Umati-UGradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, filters["ugrad_only"], remove_kurtis]), "Umati-NC-UGradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["grad_only"], remove_kurtis]), "Umati-GradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, filters["grad_only"], remove_kurtis]), "Umati-NC-GradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["staff_only"], remove_kurtis]), "Umati-StaffOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, filters["staff_only"], remove_kurtis]), "Umati-NC-StaffOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["new_to_crowdsourcing"], remove_kurtis]), "Umati-Hasn'tCrowd:"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["knows_crowdsourcing"], remove_kurtis]), "Umati-KnowsCrowdsourcing"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["EE_only"], remove_kurtis]), "Umati-EE"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["CS_only"], remove_kurtis]), "Umati-CS"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["biz_only"], remove_kurtis]), "Umati-Biz"))
        ops.append((umati_db, partial(chain_filters, filters=[filters["other_dept_only"], remove_kurtis]), "Umati-OtherDept"))

    if (kurtis_db):
        ops.append((kurtis_db, lambda x: True, "Kurtis:"))
    if (turk_db):
        ops.append((turk_db, lambda x: True, "Turkers:"))
    if (expert_db):
        ops.append((expert_db, lambda x: True, "Turkers:"))

    for (db, filt, tag) in ops:
        res.append((munge_per_question(db, filt), tag))
    for ((b_stat, per_q_stat), tag) in res:
        print (tag)
        print (b_stat)
    print ("")
    for q in all_questions:
        print (q)
        for ((b_stat, per_q_stat), tag) in res:
            if (q in per_q_stat):
                print (tag + str(per_q_stat[q]))
        print("")
            
start()
