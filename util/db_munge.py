#!/usr/bin/python

import sys, pickle, getopt
sys.path.append("..")
from umati import UmatiUserDirectory

from scipy.stats import stats, morestats
from numpy import *
from functools import partial

from lib2to3.fixes.fix_imports import MAPPING

opts, args = getopt.getopt(sys.argv[1:], 
                           "u:k:t:e:h", ["umati_db=", "kurtis_db=", "turk_db=", "expert_db="])

umati_db = None
kurtis_db = None
turk_db = None
expert_db = None

def usage():
    print ("The Umati Vending Machine User Interface")
    print ("-h | --help Show this message")
    print ("-l LOGLEVEL | --logLevel=[DEBUG|INFO|WARNING|ERROR|CRITICAL] Default is INFO")
    print ("-c CONF | --conf=Conf File location")
    exit(2)

for o,a in opts:
    if o in ("-u", "--umati_db="):
        umati_db = a
    elif o in ("-k", "--kurtis_db="):
        kurtis_db = a
    elif o in ("-t", "--turk_db="):
        turk_db = a
    elif o in ("-e", "--expert_db="):
        expert_db = a
    else:
        usage()

def normalizeDB(db):
    for user in db.values():
        if "Grading" in user.tasks_completed:
            for i in range(0, len(user.tasks_completed["Grading"])):
                cur = user.tasks_completed["Grading"][i]
                user.tasks_completed["Grading"][i] = (cur[0][-13:], cur[1], cur[2])
    return db

REVERSE_MAPPING={}
for key,val in MAPPING.items():
    REVERSE_MAPPING[val]=key

class Python_3_Unpickler(pickle.Unpickler):
    """Class for pickling objects from Python 3"""
    def find_class(self,module,name):
        if module in REVERSE_MAPPING:
            module=REVERSE_MAPPING[module]
        __import__(module)
        mod = sys.modules[module]
        klass = getattr(mod, name)
        return klass

def loads(f):
    return Python_3_Unpickler(f).load()  

if (umati_db):
    umati_db = normalizeDB(loads(open(umati_db, 'rb')))
if (kurtis_db):
    kurtis_db = normalizeDB(loads(open(kurtis_db, 'rb')))
if (turk_db):
    turk_db = normalizeDB(loads(open(turk_db, 'rb')))
if (expert_db):
    expert_db = normalizeDB(loads(open(expert_db, 'rb')))

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

def chain_filters(user, filters = []):
    for filt in filters:
        if not (filt(user)):
            return False
    return True

def remove_cheaters(user):
    return user.gold_wrong < 2

def remove_kurtis(user):
    return ";019582227=1140?" not in user.tag

#fix this later
def cs_only(user):
    if "Linear_Survey" in user.tasks_completed:
        task = user.tasks_completed["Linear_Survey"][0]
        return (get_department(task[0], task[1]) == "CS")
    return False

def ugrad_only(user):
    if "Linear_Survey" in user.tasks_completed:
        task = user.tasks_completed["Linear_Survey"][0]
        return (get_relationship(task[0], task[1]) == "Undergraduate Student")
    return False

def grad_only(user):
    if "Linear_Survey" in user.tasks_completed:
        task = user.tasks_completed["Linear_Survey"][0]
        return (get_relationship(task[0], task[1]) == "Graduate Student")
    return False

def staff_only(user):
    if "Linear_Survey" in user.tasks_completed:
        task = user.tasks_completed["Linear_Survey"][0]
        return (get_relationship(task[0], task[1]) == "Staff")
    return False

def start():
    ops = []
    res = []
    if (umati_db):
        ops.append((umati_db, remove_kurtis, "Umati-All:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_kurtis, remove_cheaters]), "Umati-NC-All:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, cs_only, remove_kurtis]), "Umati-NC-CSOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, ugrad_only, remove_kurtis]), "Umati-NC-UGradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, grad_only, remove_kurtis]), "Umati-NC-GradOnly:"))
        ops.append((umati_db, partial(chain_filters, filters=[remove_cheaters, staff_only, remove_kurtis]), "Umati-NC-GradOnly:"))
    if (kurtis_db):
        ops.append((kurtis_db, lambda x: True, "Kurtis:"))
    if (turk_db):
        ops.append((turk_db, lambda x: True, "Turkers:"))
    if (turk_db):
        ops.append((expert_db, lambda x: True, "Turkers:"))

    for (db, filt, tag) in ops:
        res.append((munge_per_question(db, filt), tag))
    for ((b_stat, per_q_stat), tag) in res:
        print (tag)
        print (b_stat)
    for q in all_questions:
        print (q)
        for ((b_stat, per_q_stat), tag) in res:
            if (q in per_q_stat):
                print (tag + str(per_q_stat[q]))
            
    #for q, res in per_q_db.iteritems():
    #    print ("Question:" + q)
    #    print ("Basic:" + str(res))
    #    if (q in per_q_nocheat_db):
    #        print ("No Cheat:" + str(per_q_nocheat_db[q]))
    #    if (q in per_q_nocheat_ugrad_db):
    #        print ("Ugrad Only-No Cheat:" + str(per_q_nocheat_ugrad_db[q]))
    #    if (q in per_q_nocheat_grad_db):
    #        print ("Grad Only-No Cheat:" + str(per_q_nocheat_grad_db[q]))

def get_gender(surv_type, surv_str):
    dic = {"0":"Male",
           "1":"Female",
           "2":"Other"}
    return dic[surv_str[1]]

def get_age(surv_type, surv_str):
    dic = None
    if (surv_type == "Intro"):
        dic = {"0":"0-18",
               "1":"18-22",
               "2":"22-39",
               "3":"40-59",
               "4":"60+"}
    elif(surv_type == "Intro2"):
        dic = {"0":"0-18",
               "1":"18-20",
               "2":"21-24",
               "3":"25-39",
               "4":"40+"}
    return dic[surv_str[4]]
        
#add original survey
def get_ed(surv_type, surv_str):
    dic = None
    if (surv_type == "Intro"):
        dic = {"0":"High School",
               "1":"Bachelors",
               "2":"Masters",
               "3":"PhD"}
    elif (surv_type == "Intro2"):
        dic = {"0":"High School",
               "1":"Associates",
               "2":"Bachelors",
               "3":"Masters",
               "4":"PhD"}
    return dic[surv_str[7]]

def get_relationship(surv_type, surv_str):
    dic = {"0":"Undergraduate Student",
           "1":"Graduate Student",
           "2":"Professor",
           "3":"Staff",
           "4":"Other"}
    return dic[surv_str[10]]

def get_department(surv_type, surv_str):
    dic = {"0":"EE",
           "1":"CS",
           "2":"Business School",
           "3":"Other Department on Campus",
           "4":"Not Related"}
    return dic[surv_str[13]]

start()
