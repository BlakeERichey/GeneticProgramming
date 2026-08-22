import numpy as np
import gymnasium as gym
from tpcomp.inference import Topology
from tpcomp.solver import Genome
from datetime import datetime
import logging
logging.getLogger().setLevel(logging.DEBUG)

genome = Genome(n_obs=16, n_act=5)
print(genome.actions)
print(genome.observations)
print(genome.lut)
print(genome.lut.lookup([True, False, False, False, True], 4))
top = Topology(genome)

stream = [8, 13, 14]
top.stage(stream)
print(top.signals)
print(top.response())
print(top._energy_history)
top.reset()

stream = np.random.randint(0, 16, 256)
top.stage(stream)
print(top.signals)
response = top.response()
print(response)
print(response.most_common())
print(top._energy_history)

# print(top)