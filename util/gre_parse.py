#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\([A|B|C|D|E]\) (.*)\n')

output = 'output.xml'
cur = ''

out = open(output, 'w')

for line in open(sys.argv[1]):
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        out.write("</question>\n")
    elif (y):
        if (cur != ''):
            out.write('<question text="%s">\n' % cur)
            cur = ''
        out.write('<answer text="%s"/>\n' % y.group(1))
    else:
        cur += line.strip()
