#!/usr/bin/python

import sys, pickle, getopt
from filters import *

opts, args = getopt.getopt(sys.argv[1:], 
                           "u:k:t:e:h", ["umati_db=", "kurtis_db=", "turk_db=", "expert_db="])

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
        umati_db = a
    elif o in ("-k", "--kurtis_db="):
        kurtis_db = a
    elif o in ("-t", "--turk_db="):
        turk_db = a
    elif o in ("-e", "--expert_db="):
        expert_db = a
    elif o in ("-o", "--output="):
        output = a
    else:
        usage()

if not (output):
    usage()
