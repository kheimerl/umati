#!/usr/bin/python

import sys, pickle
sys.path.append("..")
from umati import UmatiUserDirectory

from scipy.stats import stats, morestats
from numpy import *
from functools import partial

from lib2to3.fixes.fix_imports import MAPPING

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

load = sys.argv[1]

db = loads(open(load, 'rb'))

def munge_per_question(user_db, filter_func = lambda x: True):
    res = {}
    for user in user_db.values():
        if filter_func(user) and "Grading" in user.tasks_completed:
            for question in user.tasks_completed["Grading"]:
                if question[0] not in res:
                    res[question[0]] = []
                res[question[0]].append(int(question[1]))
    for tag in res.keys():
        t = array(res[tag])
        res[tag] = (t.mean(), t.std(), stats.stderr(t), 
                    t.var(), t.size)#, morestats.bayes_mvs(t))
    return res

def munge_basic_stats(user_db, filter_func = lambda x: True):
    (num_users, num_qs) = (0,0)
    for user in user_db.values():
        if filter_func(user):
            num_users += 1
            if "Grading" in user.tasks_completed:
                num_qs += len(user.tasks_completed["Grading"])
    return (num_users, num_qs)
            
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
        return (user.tasks_completed["Linear_Survey"][0][1][13] == "1")
    return False
        
#basic stats
basic = munge_basic_stats(db, filter_func = remove_kurtis)
print (basic)
basic_nocheat = munge_basic_stats(db, filter_func = partial(chain_filters, filters=[remove_kurtis, remove_cheaters]))
print(basic_nocheat)

per_q = munge_per_question(db, filter_func = remove_kurtis)
per_q_nocheat = munge_per_question(db, filter_func = partial(chain_filters, filters=[remove_kurtis, remove_cheaters]))
per_q_nocheat_cs = munge_per_question(db, filter_func = partial(chain_filters, filters=[remove_cheaters, cs_only, remove_kurtis]))
for q, res  in per_q.iteritems():
    print ("Question:" + q)
    print ("Basic:" + str(res))
    if (q in per_q_nocheat):
        print ("No Cheat:" + str(per_q_nocheat[q]))
    if (q in per_q_nocheat_cs):
        print ("CS Only-No Cheat:" + str(per_q_nocheat_cs[q]))
