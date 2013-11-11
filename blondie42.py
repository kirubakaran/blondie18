#!/home/kiru/pyenv/neuro2/bin/python

import random
import pybrain

from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

class BlondieBrain:
    def __init__(self,insize=150):
        self.insize = insize
        self.nn = FeedForwardNetwork()

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

    def printit(self):
        print self.nn
    
inp = [random.randint(0,6) for _ in range(150)]
print inp

n = BlondieBrain()
n.activate(inp)
n.printit()
