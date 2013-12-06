#!/usr/bin/env python

import random
import datetime
import re
import os
import heapq
import copy
import argparse
import sys
import ConfigParser
from pprint import pprint as pp

from blondiebrain import BlondieBrain, latestblondies
import runner

def rungame(b1,b2,show=False):
    score = [0,0]
    g = runner.Game()
    while True:
        for i,b in enumerate([b1,b2]):
            m = b.nextmove(g)
            try:
                if m<0 or m>6:
                    raise ValueError
                g.push_move(m)
            except ValueError:
                score[i] += int(CONFIG['points_invalidmove'])
                if show:
                    g.print_grid()
                    print "Invalid move:",m
                return score
            else:
                score[i] += int(CONFIG['points_validmove'])
            if g.is_won():
                score[i] += int(CONFIG['points_winner'])
                if show:
                    g.print_grid()
                return score

def main(loadfromdisk=False):
    popsize   = int(CONFIG['popsize'])
    keepratio = float(CONFIG['keepratio'])
    randratio = float(CONFIG['randratio'])
    maxgen    = int(CONFIG['maxgen'])
    outsize   = int(CONFIG['outsize'])
    if loadfromdisk:
        lastn = int(popsize*keepratio)
        blondiefiles = latestblondies(CONFIG['datadir'],lastn)
        print "Loading files:"
        pp(blondiefiles)
        print
        pop = []
        for bf in blondiefiles:
            pop.append(BlondieBrain(datadir=CONFIG['datadir'],paramfile=bf,outsize=outsize))
        if len(pop) < popsize:
            for i in range(popsize-len(pop)):
                bb = BlondieBrain(datadir=CONFIG['datadir'],outsize=outsize)
                bb.mutate()
                pop.append(bb)
        try:
            last = blondiefiles[-1]
            gentxt = re.search('blondie-(.*)-gen(.*).xml',last).group(2)
            print "Loaded Generation",gentxt
            gen = int(gentxt) + 1
        except IndexError:
            gen = 0
        except AttributeError:
            gen = 0
    else:
        gen = 0
        pop = [BlondieBrain(CONFIG['datadir'],outsize=outsize) for _ in range(popsize)]
    while gen < maxgen:
        print "Generation : %s"%(gen,)
        r = [0]*popsize
        for i in range(popsize):
            for j in range(popsize):
                if i == j: continue
                score = rungame(pop[i],pop[j])
                r[i] += score[0]
                r[j] += score[1]

        #write best to disk
        win  = r.index(max(r))
        print "%03d won gen %05d with %d points"%(win,gen,max(r))
        best = pop[win]
        if gen%int(CONFIG['gen_per_save']) == 0:
            best.save('-bestof-gen%05d'%(gen,))
            print "Wrote to disk (%s)"%(CONFIG['datadir'],)
        
        #rerun prev best and current best
        #to show in output
        if win == 0:
            vmsg = "*  Defending champion retains the title!  *"
            print "*"*len(vmsg)
            print vmsg
            print "*"*len(vmsg)
        msg =  "Game with defending champion playing %s and current champion playing %s"
        print msg%(0,1)
        sc0,sc1 = rungame(pop[0],pop[win],show=True)
        #print "Scores:",sc0,sc1
        print msg%(1,0)
        sc1,sc0 = rungame(pop[win],pop[0],show=True)
        #print "Scores:",sc1,sc0
        print

        #keep top best for next gen
        bestn = heapq.nlargest(int(popsize*keepratio),r)
        newpop = []
        for x in bestn:
            #print "copying %02d to next gen as %d"%(r.index(x),len(newpop))
            newpop.append(pop[r.index(x)].copy())

        #throw in some wildcards
        for x in range(int(popsize*randratio)):
            t = best.copy()
            t.randomize()
            newpop.append(t)
            
        #mutate best to fill rest of the spots
        spotsleft = popsize - len(newpop)
        for n in range(spotsleft):
            t = best.copy()
            t.mutate()
            newpop.append(t)
        pop = newpop
        gen += 1
            
if __name__ == '__main__':
    global CONFIG
    parser = argparse.ArgumentParser(description='Create Connect-4 AI Players')
    parser.add_argument('--loadfromdisk',required=False,action='store_true')
    parser.add_argument('--configsection',required=True,help='Name of the config section in ./config to use. You can say: default')
    args = vars(parser.parse_args())
    loadfromdisk = args['loadfromdisk']

    # read configuration
    c = args['configsection']
    cf = ConfigParser.ConfigParser()
    cf.read('blondie.conf')
    CONFIG = dict(cf.items('default'))
    config_custom  = dict(cf.items(c))
    for k,v in config_custom.iteritems():
        CONFIG[k] = v

    if not os.path.exists(CONFIG['datadir']):
        print "Please create",CONFIG['datadir']
        print "Exiting ..."
        sys.exit()

    print "Best of every %s generations will be saved to disk"%(CONFIG['gen_per_save'])
        
    main(loadfromdisk)
