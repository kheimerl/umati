#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\(([A|B|C|D|E|T])\) (.*)\n')

HEADER = re.compile('^([0-9]*)\)(.*)')

cur = ''
print('<h3>Answer these questions</h3>')

count = 0
for line in open(sys.argv[1]):
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        print("<br>\n")
    elif (y):
        if (cur != ''):
            
            z = HEADER.match(cur)
            
            # print('<p>%s</p>' % cur.strip())
            print('<p>%s</p>' % z.group(2))
            cur = ''
            count += 1
        val = y.group(2)
        print('<input type="checkbox" value="%s" name="%d"/>%s<br>' % (val, count, val))
    else:
        cur += line

print('<br>')
