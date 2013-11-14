#!/usr/bin/env python

import random
import datetime
import re
import os
import itertools
import heapq
import copy
import argparse
from pprint import pprint as pp

from pybrain.structure import FeedForwardNetwork, \
     LinearLayer, SigmoidLayer, FullConnection

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader

import runner
import config

class BlondieBrain:
    def __init__(self,insize=None,paramfile=None,datadir=config.DATADIR):
        self.datadir = datadir
        if insize == None:
            g = runner.Game()
            ip = self._game2input(g)
            self.insize = len(ip)
        else:
            self.insize = insize
        if paramfile:
            f = os.path.join(datadir,paramfile)
            self.nn = NetworkReader.readFrom(f)
            try:
                self.name = re.search('(.*)-bestof-(.*)',paramfile).group(1)
            except AttributeError:
                self.name = "blondie-%s"%(datetime.datetime.now())
        else:
            self.nn = FeedForwardNetwork()
            tmpname = "blondie-%s"%(datetime.datetime.now())
            self.name = re.sub('[.: ]', '-', tmpname)

            inLayer = LinearLayer(self.insize)
            hiddenLayer1 = SigmoidLayer(self.insize)
            hiddenLayer2 = SigmoidLayer(self.insize)
            outLayer = LinearLayer(1)

            self.nn.addInputModule(inLayer)
            self.nn.addModule(hiddenLayer1)
            self.nn.addModule(hiddenLayer2)
            self.nn.addOutputModule(outLayer)

            in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
            hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
            hidden2_to_out = FullConnection(hiddenLayer2, outLayer)

            self.nn.addConnection(in_to_hidden1)
            self.nn.addConnection(hidden1_to_hidden2)
            self.nn.addConnection(hidden2_to_out)

            self.nn.sortModules()

    def nextmove(self,game):
        inputdata = self._game2input(game)
        return int(self.nn.activate(inputdata))

    def save(self,suffix=''):
        f = os.path.join(self.datadir,self.name+suffix+".xml")
        NetworkWriter.writeToFile(self.nn, f)

    def mutate(self):
        self.nn.mutate()

    def randomize(self):
        self.nn.randomize()        
        
    def copy(self):
        x = copy.deepcopy(self)
        x.nn = x.nn.copy()
        return x

    @classmethod
    def _game2input(cls,game):
        mysymbol = len(game.moves)%2
        cells = [cls._trsymb(x,mysymbol) for x in itertools.chain.from_iterable(game.grid_columns)]
        cols  = [cls._trsum(c,mysymbol)  for c in game.grid_columns]
        rows  = [cls._trsum(r,mysymbol)  for r in game.grid_rows]
        diags = [cls._trsum(r,mysymbol)  for r in game.diags]
        l = itertools.chain.from_iterable([cells,cols,rows,diags])
        return list(l)

    @classmethod
    def _trsymb(cls,piece,mysymbol):
        #Transform symbol
        if piece == None:
            return 0
        elif piece == mysymbol:
            return 1
        else:
            return -1

    @classmethod
    def _trsum(cls,l,mysymbol):
        #Transform symbol and sum list
        s = 0
        for ll in l:
            s += cls._trsymb(ll,mysymbol)
        return s

def rungame(b1,b2):
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
                score[i] += config.points['invalidmove']
                return score
            else:
                score[i] += config.points['validmove']
            if g.is_won():
                score[i] += config.points['winner']
                #print "We have a winner"
                #g.print_grid()
                return score

def getgen(f):
    #get generation number from filename
    gen = re.search('(.*)-bestof-gen(.*).xml',f).group(2)
    if gen:
        return int(gen)
    else:
        return 0
            
def main(loadfromdisk=False):
    if loadfromdisk:
        blondiefiles = sorted([f for f in os.listdir(config.DATADIR) if f.startswith('blondie-')],key=getgen)
        pop = []
        print "Loading files:"
        pp(blondiefiles[-config.popsize:])
        print
        lastn = int(config.popsize*config.keepratio)
        for bf in blondiefiles[-lastn:]:
            pop.append(BlondieBrain(paramfile=bf))
        if len(pop) < config.popsize:
            for i in range(config.popsize-len(pop)):
                bb = BlondieBrain()
                bb.mutate()
                pop.append(bb)
        try:
            gentxt = re.search('blondie-(.*)-gen(.*).xml',last).group(2)
            print "Loaded Generation",gentxt
            gen = int(gentxt) + 1
        except AttributeError:
            gen = 0
    else:
        gen = 0
        pop = [BlondieBrain() for _ in range(config.popsize)]
    while gen < config.maxgen:
        print "Generation : %s"%(gen,)
        r = [0]*config.popsize
        for i in range(config.popsize):
            for j in range(config.popsize):
                if i == j: continue
                score = rungame(pop[i],pop[j])
                r[i] += score[0]
                r[j] += score[1]
                
        #write best to disk
        win  = r.index(max(r))
        print "%03d won gen %05d with %d points"%(win,gen,max(r))
        best = pop[win]
        best.save('-bestof-gen%05d'%(gen,))
        
        #keep top best for next gen
        bestn = heapq.nlargest(int(config.popsize*config.keepratio),r)
        newpop = []
        for x in bestn:
            newpop.append(pop[r.index(x)].copy())

        #throw in some wildcards
        wildn = bestn
        for x in wildn:
            t = best.copy()
            t.randomize()
            newpop.append(t)
            
        #mutate best to fill rest of the spots
        spotsleft = config.popsize - len(newpop)
        for n in range(spotsleft):
            t = best.copy()
            t.mutate()
            newpop.append(t)
        pop = newpop
        gen += 1
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Connect-4 AI Players')
    parser.add_argument('--loadfromdisk',required=False,action='store_true')
    args = vars(parser.parse_args())
    loadfromdisk = args['loadfromdisk']
    main(loadfromdisk)
