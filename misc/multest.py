#!/usr/bin/env python

# try to get to c = 0.25a + 0.75b
#

import random
from pprint import pprint as pp

gen = 0

pop = []
for p in range(10):
    nw = []
    for i in range(3):
        nwr = []
        for j in range(2):
            x = random.random()
            nwr.append(x)
        nw.append(nwr)
    pop.append(nw)

print "Initial Population:"
pp(pop)
print
        
# test = []
# for i in range(10):
#     x = random.randrange(100)
#     y = random.randrange(100)
#     z = 0.25*x + 0.75*y
#     test.append([x,y,z])

# print "Test Set:"
# pp(test)
# print

t = [15, 77, (0.25*15 + 0.75*77)]

def nweval(in_nw,in_1,in_2):
    x,y=1,1
    for i,r in enumerate(in_nw):
        f1 = r[0]
        f2 = r[1]
        if i%2 == 0:
            x = x*f1
            y = y*f2
        else:
            if x > f1:
                x = 1
            else:
                x = 0
            if y > f2:
                y = 1
            else:
                y = 0
    z = x+y
    print "nweval :",z
    return z

while gen < 10:
    delta = []
    for zpop in pop:
        rslt = nweval(zpop,t[0],t[1])
        delta.append(abs(t[2] - rslt))
    # eliminate worst 3
    for e in range(3):
        ep = delta.index(max(delta))
        pop.pop(ep)
    # reproduce 3 best
    rp = delta.index(min(delta))
    for e in range(3):
        #print "rp",rp
        rp_nw = pop[rp][:][:]
        for r in range(len(rp_nw)):
            for c in range(len(rp_nw[0])):
                #roll dice
                d = random.randrange(6)
                print d
                if d <= 3:
                    rp_nw[r][c] *= (random.random() * 2)
        pop.append(rp_nw)
    print "Generation :",gen
    #pp(pop)
    print "Deltas :",delta
    print "-"*60
    print
    gen += 1

