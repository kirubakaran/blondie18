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
    def __init__(self,insize=139,paramfile=None,datadir=DATADIR):
        self.datadir = datadir
        if paramfile:
            f = os.path.join(datadir,paramfile)
            self.nn = NetworkReader.readFrom(f)
            self.name = paramfile.split('.')[0]
        else:
            self.insize = insize
            self.nn = FeedForwardNetwork()
            tmpname = "blondie-%s"%(datetime.datetime.now())
            self.name = re.sub('[.: ]', '-', tmpname)

            inLayer = LinearLayer(insize)
            hiddenLayer1 = SigmoidLayer(insize)
            hiddenLayer2 = SigmoidLayer(insize)
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

    def nextmove(self,inputdata):
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

def trsymb(piece,mysymbol):
    #Transform symbol
    if piece == None:
        return 0
    elif piece == mysymbol:
        return 1
    else:
        return -1

def trsum(l,mysymbol):
    #Transform symbol and sum list
    s = 0
    for ll in l:
        s += trsymb(ll,mysymbol)
    return s

def game2input(game):
    mysymbol = len(game.moves)%2
    cells = [trsymb(x,mysymbol) for x in itertools.chain.from_iterable(game.grid_columns)]
    cols  = [trsum(c,mysymbol) for c in game.grid_columns]
    rows  = [trsum(r,mysymbol) for r in game.grid_rows]
    diags = [trsum(r,mysymbol) for r in game.diags]
    l = itertools.chain.from_iterable([cells,cols,rows,diags])
    return list(l)

def rungame(b1,b2):
    return (random.randint(0,5),random.randint(0,5))

def main(game):
    gen = 0
    popsize = 20
    pop = [BlondieBrain() for _ in range(100)]

    #while gen > 10: #disabled
    while gen < 10:
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
        #keep best 10% for next gen
        bestn = heapq.nlargest(int(popsize/10.0),r)
        print "bestn",bestn
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
        
    # n = BlondieBrain()
    # for i in range(10):
    #     ip = game2input(game)
    #     print "m1", i, "move = ", n.nextmove(ip)
    # n.save('-m1')
    # n.nn.mutate()
    # print('')
    # for i in range(10):
    #     ip = game2input(game)
    #     print "m2", i, "move = ", n.nextmove(ip)
    # n.save('-m2')
    
    # n = BlondieBrain()
    # ip = game2input(game)
    # #x = [copy.deepcopy(n) for _ in range(2)]
    # x = [n.copy() for _ in range(2)]
    # #x = [n for _ in range(10)]
    # for xx in x:
    #     print id(xx)
    #     print ">",xx.nextmove(ip)
    #     xx.mutate()
    #     print "<",xx.nextmove(ip)
    # print
    # for xx in x:
    #     print id(xx)
    #     print xx.nextmove(ip)
    # print "m1 move = ", n.nextmove(ip)
    # m = copy.deepcopy(n)
    # m.nn.mutate()
    # ip = game2input(game)
    # print "m2 move = ", m.nextmove(ip)

    # ip = game2input(game)
    # n = [BlondieBrain() for _ in range(10)]
    # for i in range(10):
    #     for nnx in n:
    #         print nnx.nextmove(ip),
    #         nnx.mutate()
    #     print
    
if __name__ == '__main__':
    game = runner.Game()
    
    # g.push_move(1)
    # game2input(g)
    # g.push_move(1)
    # game2input(g)
    
    main(game)
