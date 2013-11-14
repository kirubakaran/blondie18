#!/home/kiru/pyenv/neuro2/bin/python

import runner
from genblondie import BlondieBrain

import os
import re
import csv
from collections import defaultdict

DATADIR = "/media/tera/blondiehome"

def getwinner(b1,b2):
    g = runner.Game()
    while True:
        for i,b in enumerate([b1,b2]):
            m = b.nextmove(g)
            try:
                if m<0 or m>6:
                    raise ValueError
                g.push_move(m)
            except ValueError:
                return abs(i-1)
            else:
                pass
            if g.is_won():
                return i

def main():
    bf = sorted(os.listdir(DATADIR),key=os.path.getctime)
    bf = [f for f in bf if f.startswith('blondie-')]
    print bf[-20:]
    print "-"*60
    bf = sorted([ f for f in os.listdir(DATADIR) if f.startswith('blondie-')])
    print bf[-20:]
    import sys
    sys.exit()
    #bf = bf[:20]
    lb = len(bf)
    resultcnt     = defaultdict(int)
    resultwonover = defaultdict(list)
    for i in range(lb):
        for j in range(lb):
            if i == j: continue
            b1 = BlondieBrain(paramfile=bf[i])
            b1name = re.search('blondie-(.*)-gen(.*).xml',bf[i]).group(2)
            b2 = BlondieBrain(paramfile=bf[j])
            b2name = re.search('blondie-(.*)-gen(.*).xml',bf[j]).group(2)
            print b1name,"vs",b2name
            w = getwinner(b1,b2)
            winner = [b1name,b2name][w]
            loser = [b1name,b2name][abs(w-1)]
            resultcnt['B'+winner] += 1
            resultwonover['B'+winner].append('B'+loser)
            print winner,"wins"
            print

    f = os.path.join(DATADIR,"fightreport-score-2013nov11-1712.csv")
    print "Writing",f
    with open(f, 'wb') as fp:
        writer = csv.writer(fp)
        for k,v in resultcnt.iteritems():
            writer.writerow([k , str(v) , ' '.join(resultwonover[k])])
            
if __name__ == '__main__':
    main()
