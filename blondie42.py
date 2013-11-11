#!/home/kiru/pyenv/neuro2/bin/python

import random
import datetime
import re
import os
import itertools
import heapq
import copy

from pybrain.structure import FeedForwardNetwork, \
     LinearLayer, SigmoidLayer, FullConnection

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader

import runner

DATADIR = "/media/tera/blondiehome"
     
class BlondieBrain:
    def __init__(self,insize=None,paramfile=None,datadir=DATADIR):
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
            self.name = paramfile.split('.')[0]
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

    def copy(self):
        x = copy.deepcopy(self)
        x.nn = x.nn.copy()
        return x

    def _game2input(self,game):
        mysymbol = len(game.moves)%2
        cells = [self._trsymb(x,mysymbol) for x in itertools.chain.from_iterable(game.grid_columns)]
        cols  = [self._trsum(c,mysymbol)  for c in game.grid_columns]
        rows  = [self._trsum(r,mysymbol)  for r in game.grid_rows]
        diags = [self._trsum(r,mysymbol)  for r in game.diags]
        l = itertools.chain.from_iterable([cells,cols,rows,diags])
        return list(l)
        
    def _trsymb(piece,mysymbol):
        #Transform symbol
        if piece == None:
            return 0
        elif piece == mysymbol:
            return 1
        else:
            return -1
     
    def _trsum(l,mysymbol):
        #Transform symbol and sum list
        s = 0
        for ll in l:
            s += trsymb(ll,mysymbol)
        return s

def rungame(b1,b2):
    return (random.randint(0,5),random.randint(0,5))

def main(game):
    popsize   = 20
    keepratio = 10.0/100.0 #ratio of top performers to keep
    maxgen    = 10

    gen = 0
    pop = [BlondieBrain() for _ in range(popsize)]
    while gen < maxgen:
        print "Generation : %s"%(gen,)
        r = [0]*popsize
        for i in range(popsize):
            for j in range(popsize):
                if i == j: continue
                ri,rj = rungame(pop[i],pop[j])
                r[i] += ri
                r[j] += rj
                
        #write best to disk
        win  = r.index(max(r))
        print "winner of gen %03d is %02d"%(gen,win)
        best = pop[win]
        best.save('-bestof-gen%03d'%(gen,))
        
        #keep top best for next gen
        bestn = heapq.nlargest(int(popsize*keepratio),r)
        newpop = []
        for x in bestn:
            newpop.append(pop[r.index(x)].copy())
        spotsleft = popsize - len(newpop)
        for n in range(spotsleft):
            t = best.copy()
            t.mutate()
            newpop.append(t)
        pop = newpop
        gen += 1
            
if __name__ == '__main__':
    main()
