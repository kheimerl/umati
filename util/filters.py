from functools import partial

#filters
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

def get_crowdsourcing_knowledge(surv_type, surv_str):
    dic = {"0":"Yes",
           "1":"No"}
    return dic[surv_str[16]]

def get_crowdsourcing_use(surv_type, surv_str):
    dic = {"0":"Yes, created tasks",
           "1":"Yes, completed tasks",
           "2":"Yes, created and completed tasks",
           "3":"No",
           "4":"Maybe, Not Sure"}
    return dic[surv_str[19]]

def chain_filters(user, filters = []):
    for filt in filters:
        if not (filt(user)):
            return False
    return True

def remove_cheaters(user):
    return user.gold_wrong < 2

def remove_kurtis(user):
    return ";019582227=1140?" not in user.tag

filters = {}

def basic_filter(user, func=None, expect=None):
    if "Linear_Survey" in user.tasks_completed:
        task = user.tasks_completed["Linear_Survey"][0]
        return (func(task[0], task[1]) == expect)
    return False

for (func, expect, name) in [(get_department, "CS", "cs_only"),
                             (get_relationship, "Undergraduate Student", "ugrad_only"),
                             (get_relationship, "Graduate Student", "grad_only"),
                             (get_relationship, "Staff", "staff_only"),
                             (get_crowdsourcing_knowledge, "Yes", "knows_crowdsourcing"),
                             (get_crowdsourcing_use, "No", "new_to_crowdsourcing")]:
    filters[name] = partial(basic_filter, func=func, expect=expect)


