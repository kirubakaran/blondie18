#!/home/kiru/pyenv/neuro2/bin/python

import random
import math

# import matplotlib
# from pylab import plot, legend, subplot, grid, xlabel, ylabel, show, title
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from pyneurgen.neuralnet import NeuralNet
from pyneurgen.nodes import BiasNode, Connection

# all samples are drawn from this population
pop_len = 200

factor = 1.0 / float(pop_len)
# population = [[i, math.sin(float(i) * factor * 10.0) + \
#                 random.gauss(float(i) * factor, .2)]
#                     for i in range(pop_len)]
population = [[i, float(i**2)]
                    for i in range(pop_len)]

all_inputs = []
all_targets = []

def population_gen(population):
    pop_sort = [item for item in population]
    random.shuffle(pop_sort)

    for item in pop_sort:
        yield item

#   Build the inputs
for position, target in population_gen(population):
    pos = float(position)
    all_inputs.append([random.random(), pos * factor])
    all_targets.append([target])

net = NeuralNet()
net.init_layers(2, [10], 1)

net.randomize_network()
net.set_halt_on_extremes(True)

#   Set to constrain beginning weights to -.5 to .5
#       Just to show we can
net.set_random_constraint(.5)
net.set_learnrate(.1)

net.set_all_inputs(all_inputs)
net.set_all_targets(all_targets)

length = len(all_inputs)
learn_end_point = int(length * .8)

net.set_learn_range(0, learn_end_point)
net.set_test_range(learn_end_point + 1, length - 1)

net.layers[1].set_activation_type('tanh')

net.learn(epochs=125, show_epoch_results=True,
    random_testing=False)

mse = net.test()

test_positions = [item[0][1] * 1000.0 for item in net.get_test_data()]

all_targets1 = [item[0][0] for item in net.test_targets_activations]
allactuals = [item[1][0] for item in net.test_targets_activations]

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot([i[1] for i in population])
ax1.set_title("Population")
ax1.grid(True)

ax2 = fig.add_subplot(312)
ax2.plot(test_positions, all_targets1, 'bo', label='targets')
ax2.plot(test_positions, allactuals, 'ro', label='actuals')
ax2.grid(True)
ax2.legend(loc='lower left', numpoints=1)
ax2.set_title("Test Target Points vs Actual Points")

ax3 = fig.add_subplot(313)
ax3.plot(range(1, len(net.accum_mse) + 1, 1), net.accum_mse)
ax3.set_xlabel('epochs')
ax3.set_ylabel('mean squared error')
ax3.grid(True)
ax3.set_title("Mean Squared Error by Epoch")

plt.show()

