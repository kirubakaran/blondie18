#!/home/kiru/pyenv/neuro2/bin/python

import random
import datetime
import re
import os
import itertools

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

    def save(self):
        f = os.path.join(self.datadir,self.name+".xml")
        NetworkWriter.writeToFile(self.nn, f)

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
        
def main(game):
    # popsize = 100
    # pop = [BlondieBrain() for _ in range(100)]
    # print pop
    n = BlondieBrain()
    ip = game2input(game)
    print "move = ", n.nextmove(ip)
    n.save()
    
if __name__ == '__main__':
    game = runner.Game()
    
    # g.push_move(1)
    # game2input(g)
    # g.push_move(1)
    # game2input(g)
    
    main(game)
