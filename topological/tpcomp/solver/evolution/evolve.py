from .tracker import NASTracker
import tqdm
from .fitness import rank_and_influence_Fitness, get_column_min_indices
import logging
from collections import defaultdict
import numpy as np

class Population:
    def __init__(self, n, individual_cls):
        self.genotype = genotype
        self.individuals = [
            Individual(Organism(genotype).genome)
            for _ in range(n)
        ]




class EvoSolver:

    def __init__(self, population, world, witness=None):
        self.population = population
        self.environment = world
        self._generation = 0

    def evolve(self, generations=1):
        for i in range(generations):
            ranked = self.evaluate()
        mating_pool = self.selection(ranked)
        offspring = self.crossover(mating_pool)
            # self.mutate(offspring)
        self.anniversary(offspring)
            #self._generation += 1

    def evaluate(self):
        fitnesses = deque()
        with tqdm.tqdm(total=len(self.population), desc='Evaluating Population') as pbar:
            for individual in self.population.individuals:
                fitness = self.simulator.run(individual)
                fitnesses.append(fitness)
        return sorted(fitnesses, key=lambda fitness: fitness.fitness, reverse=True)

    def selection(self, ranked):
        mating_pool = []
        remaining = set([ind.uuid for ind in ranked])
        while len(remaining) > 1:
            ind = ranked.popleft()
            n_offspring = ind.num_offspring()
            candidates = remaining - ind.relatives()
            if n_offspring:
                i = np.random.randint(len(candidates))
                partner_uuid = ranked.pop(i)

                mating_pool.extend([
                    (ind, partner)
                    for _ in range(n_offspring)
                ])

    def crossover(self, mating_pool):
        offspring = []
        for (parentA, parentB) in mating_pool:
            offspring.append(
                self.population.breeder(parentA, parentB, mutate=True)
            )
        return offspring

    def anniversary(self, offspring):
        for ind in self.population:
            ind.birthday()
        
        remaining = list(filter(
            lambda ind: ind.living,
            self.population,
        ))

        self.population = remaining + offspring