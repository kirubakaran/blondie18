import itertools
import datetime
import re
import os

from pybrain.structure import FeedForwardNetwork, \
     LinearLayer, SigmoidLayer, FullConnection
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader

import runner

class BlondieBrain:
    def __init__(self,datadir,insize=None,paramfile=None):
        self.datadir = datadir
        if insize == None:
            g = runner.Game()
            ip = self._game2input(g)
            self.insize = len(ip)
        else:
            self.insize = insize
        if paramfile:
            f = os.path.join(self.datadir,paramfile)
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

# ------------------------------------------------------------

def getgen(f):
    #get generation number from filename
    gen = re.search('(.*)-bestof-gen(.*).xml',f).group(2)
    if gen:
        return int(gen)
    else:
        return 0

def latestblondies(datadir,n):
    blondiefiles = sorted([f for f in os.listdir(datadir) if f.startswith('blondie-')],key=getgen)
    return blondiefiles[-n:]
