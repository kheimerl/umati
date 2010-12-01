#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\(([A|B|C|D|E|T])\) (.*)\n')

cur = ''
print('<survey type="CSGRE" value="5">')

count = 0
for line in open(sys.argv[1]):
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        print("  </question>\n")
    elif (y):
        if (cur != ''):
            print('  <question text="%s" id="%d">' % (cur.strip(), count))
            cur = ''
            count += 1
        if (y.group(1) == "T"):
            print('    <answer text="%s" right="T"/>' % y.group(2))
        else:
            print('    <answer text="%s" right="F"/>' % y.group(2))
    else:
        cur += line

print('</survey>')
