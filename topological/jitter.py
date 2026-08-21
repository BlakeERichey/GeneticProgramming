import numpy as np
import gymnasium as gym
from tpcomp.inference import Topology
from tpcomp.solver import Genome
from datetime import datetime

genome = Genome(n_obs=1, n_act=5)
print(genome.actions)
print(genome.observations)
print(genome.lut)
# top = Topology(genome)
# print(top)