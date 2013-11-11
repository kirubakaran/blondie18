#!/home/kiru/pyenv/neuro2/bin/python

import random
import pybrain

from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

n = FeedForwardNetwork()

inLayer = LinearLayer(150)
hiddenLayer1 = SigmoidLayer(150)
hiddenLayer2 = SigmoidLayer(150)
outLayer = LinearLayer(1)

n.addInputModule(inLayer)
n.addModule(hiddenLayer1)
n.addModule(hiddenLayer2)
n.addOutputModule(outLayer)

in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
hidden2_to_out = FullConnection(hiddenLayer2, outLayer)

n.addConnection(in_to_hidden1)
n.addConnection(hidden1_to_hidden2)
n.addConnection(hidden2_to_out)

n.sortModules()

inp = [random.randint(0,6) for _ in range(150)]
print inp

x = n.activate(inp)
print n
print x
