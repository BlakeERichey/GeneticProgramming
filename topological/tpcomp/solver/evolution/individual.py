import numpy as np


class Individual:
    # ACTION LUT - TSP Constraint application
    # computational distance for a topological state
    # find the maximally distant permissible sequence of actions to define the action pool
    # this topologically enforces constraints due to time delay for realizability
    # Jitter protocol
    GENE_POOL = GenePool()
    def __init__(self, num_choromosomes, genome=None):
        if genome: 
            self.genome = genome
        else:
            self.genome = Individual.GENE_POOL.random_choromosome(num_choromosomes)

    def new_individual(self, **kwargs):
        return Individual(self.num_genes, **kwargs)

    def fitness(self, env):
        rewards = []
        ob, info = env.reset(seed=seed)
        done = truncate = False
        while not done and not truncate and not topology._abort:
            ob = safe_min_max_normalize(ob)
            state = topology.receive(ob)
            action = topology.get_action_from_state(state, env.action_space.n)
            ob, reward, done, truncate, info = env.step(action)
            rewards.append(reward)
        
        if not topology._abort:
            fitness = sum(rewards)
        else:
            fitness = -np.inf
        return fitness

