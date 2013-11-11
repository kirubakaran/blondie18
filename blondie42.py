#!/home/kiru/pyenv/neuro2/bin/python

import pybrain

import random
import datetime
import re

from pybrain.structure import FeedForwardNetwork, \
     LinearLayer, SigmoidLayer, FullConnection

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
     
class BlondieBrain:
    def __init__(self,insize=150,paramfile=None,datadir='blondiehome'):
        if paramfile:
            self.nn = NetworkReader.readFrom(paramfile)
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

    def activate(self,inputdata):
        return self.nn.activate(inputdata)

    def save(self):
        NetworkWriter.writeToFile(self.nn, "blondestore/%s.xml"%(self.name))
    
inp = [random.randint(0,6) for _ in range(150)]

n = BlondieBrain()
n.activate(inp)
n.save()
