#!/usr/bin/python

import re, sys

DELIM_RE = re.compile('QQQ\n')
ANS_PARSE = re.compile('\(([A|B|C|D|E|T])\) (.*)\n')

HEADER = re.compile('^([0-9]*)\)(.*)')

cur = ''
print('<h3>Answer these questions</h3>')

count = 0
outfile = open('umati_survey.input', 'w')
outfile.write('qid\tquestion1\tchoice1a\tchoice1b\tchoice1c\tchoice1d\tchoice1e' + '\tqid\t\tquestion2\tchoice2a\tchoice2b\tchoice2c\tchoice2d\tchoice2e' + '\tqid\t\tquestion3\tchoice3a\tchoice3b\tchoice3c\tchoice3d\tchoice3e\n')
for line in open(sys.argv[1]):
    if count == 4:
        pass
    y = ANS_PARSE.match(line)
    if (DELIM_RE.search(line)):
        if count % 3 == 0:
            outfile.write('\n')
            sys.stdout.write('\n')
    elif (y):
        if (cur != ''):
            outstr = cur.strip().replace('\t', ' ').replace('\n', '  ')
            outfile.write(str(count) + '\t' + outstr+'\t')
            sys.stdout.write(str(count) + '\t' + outstr+'\t')
            cur = ''
            count += 1
        val = y.group(2)
        val = val.strip().replace('\t', ' ').replace('\n', '  ')
        outstr = val+'\t'
        outfile.write(outstr+'\t')
        sys.stdout.write(outstr+'\t')
    else:
        cur += line
outfile.close()