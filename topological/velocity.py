import numpy as np
import gymnasium as gym
from tpcomp.inference import Topology
from tpcomp.solver import Genome
from datetime import datetime

genome = Genome(n_obs=1, n_act=5)
print(genome.actions)
print(genome.observations)
top = Topology(genome)
print(top)

stream = np.array([1, 1, 0, 0, 1, 0, 0, 0, 1])
deltas = []
for value in stream:
    start = datetime.now()
    top.receive(np.array([value]))
    end = datetime.now()
    deltas.append(end-start)
    top.render()
    print(top, '\n\n')
top.plot()
print(deltas)

# def safe_min_max_normalize(data):
#     """
#     Safely normalize a NumPy array to the range [0, 1].

#     Handles the case where all elements in the array are the same 
#     to avoid ZeroDivisionError.
#     """
#     data_min = np.min(data)
#     data_max = np.max(data)
    
#     if data_min == data_max:
#         # If all values are identical, return an array of zeros 
#         # or ones, depending on desired behavior.
#         # An array of zeros within the [0, 1] range is common.
#         return np.zeros_like(data, dtype=np.float64)
#     else:
#         return (data - data_min) / (data_max - data_min)

# def evaluate_topology(env, topology, seed=None):
#     rewards = []
#     ob, info = env.reset(seed=seed)
#     done = truncate = False
#     while not done and not truncate and not topology._abort:
#         ob = safe_min_max_normalize(ob)
#         state = topology.receive(ob)
#         action = topology.get_action_from_state(state, env.action_space.n)
#         ob, reward, done, truncate, info = env.step(action)
#         rewards.append(reward)
    
#     if not topology._abort:
#         fitness = sum(rewards)
#     else:
#         fitness = -np.inf
#     return fitness

# env_name = "MountainCar-v0"
# env = gym.make(env_name)
# evaluate_topology(env, top)