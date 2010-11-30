#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\([A|B|C|D|E]\) (.*)\n')

cur = ''
print('<survey type="CSGRE" value="5">')

for line in open(sys.argv[1]):
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        print("  </question>\n")
    elif (y):
        if (cur != ''):
            print('  <question text="%s">' % cur.strip())
            cur = ''
        print('    <answer text="%s"/>' % y.group(1))
    else:
        cur += line

print('</survey>')
