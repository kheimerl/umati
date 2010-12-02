#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\(([A|B|C|D|E|T])\) (.*)\n')

HEADER = re.compile('^([0-9]*)\)(.*)')

cur = ''
print('<h3>Answer these questions</h3>')

count = 0
outfile = open('gre0.html', 'w')
for line in open(sys.argv[1]):
    if count == 4:
        pass
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        if count % 5 == 0:
            outfile.close()
            s = str(count/5)
            outfile = open('gre'+s+'.html', 'w')
    elif (y):
        if (cur != ''):
            
            # z = HEADER.match(cur)
            
            outstr = '<p>%s</p>' % cur.strip()
            print(outstr)
            outfile.write(outstr+'\n')
            # print('<p>%s</p>' % z.group(2))
            cur = ''
            count += 1
        val = y.group(2)
        outstr = '<input type="checkbox" value="%s" name="%d"/>%s<br>' % (val, count, val)
        print(outstr)
        outfile.write(outstr+'\n')
    else:
        cur += line
outfile.close()