import random
from tqdm import tqdm
from collections import namedtuple
from itertools import product

import numpy as np

def min_max_scale(array):
    return (array - array.min()) / (array.max() - array.min())

def softmax_stable(x):
    return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

class GenePool:
    def __init__(self):
        self.valid = tuple(product(range(10), range(10)))

    def random_gene(self, k=1):
        return random.sample(self.valid, k) #without replacement

    def phenotype_from_gene(self, gene):
        index, shift = gene
        remaining = list(range(10))
        expr = remaining[index]
        phenotype = [expr]
        remaining[index] = None
        while True:
            index = (index + shift) % len(remaining)
            expr = remaining[index]
            if expr is None:
                break
            phenotype.append(expr)
            remaining[index] = None
        return phenotype

class Individual:
    GENE_POOL = GenePool()

    def __init__(self, num_genes, genome=None):
        self.num_genes = num_genes
        if genome:
            self.genome = genome
        else:
            self.genome = Individual.GENE_POOL.random_gene(k=num_genes)

    def new_individual(self, **kwargs):
        return Individual(self.num_genes, **kwargs)

    def fitness(self,):
        return sum(map(sum, map(Individual.GENE_POOL.phenotype_from_gene, self.genome)))
        # return np.prod(list(map(sum, map(Individual.GENE_POOL.phenotype_from_gene, self.genome))))

    def mutate(self, r=0.1):
        # insertion, replacement, swap with neighbor, deletion, etc..
        replacement_indices = []
        dropped_genes = set()
        for i, gene in enumerate(self.genome):

            # replacement
            if random.random() < r:
                replacement_indices.append(i)
                dropped_genes.add(gene)

        valid = set(Individual.GENE_POOL.valid).difference(set(gene)).union(dropped_genes)
        for i in replacement_indices:
            introduced = random.choice(list(valid))
            self.genome[i] = introduced
            valid = valid.difference(set(introduced))

class EvoSolver:
    def __init__(self, pop_size, n_elites, individual_cls, num_genes):
        self.n_elites   = n_elites
        self.pop_size = pop_size
        self.individual_cls = individual_cls
        self.num_genes = num_genes
        self._generation = 0

    def evaluate(self, population):
        """
        Evaluate population and rank them based on fitness function
        """
        fitnesses = []
        Fitness = namedtuple('fitness', 'index fitness')
        for i, indiv in enumerate(population):
            fitnesses.append(
            Fitness(i, indiv.fitness())
            )
        
        return sorted(fitnesses, key=lambda fitness: fitness.fitness, reverse=True)

    def crossover(self, population, ranked):
        new_pop = []
        indices = np.array([ind.index for ind in ranked])
        fitnesses = np.array([ind.fitness for ind in ranked])
        probs = min_max_scale(fitnesses)
        probs = softmax_stable(probs)

        for i in range(self.n_elites):
            new_pop.append(population[indices[i]]) #elite persists
        
        for _ in range(self.pop_size-self.n_elites):
            parent_a_i, parent_b_i = np.random.choice(indices, size=2, replace=False, p=probs)
            parentA = population[parent_a_i]
            parentB = population[parent_b_i]
            new_genome = self.splice(parentA, parentB)
            new_pop.append(parentA.new_individual(genome=new_genome))

        return new_pop

    def splice(self, parentA, parentB):
        new_genome = []
        for index in range(parentA.num_genes):
            if random.random() < 0.5:
                new_genome.append(parentA.genome[index])
            else:
                new_genome.append(parentB.genome[index])
        return new_genome


    def mutate(self, population):
        for ind in population:
            ind.mutate()

    def create_population(self):
        return [self.individual_cls(self.num_genes) for _ in range(self.pop_size)]
        

    def evolve(self, generations):
        """
        Run natural selection experiment for number of generations passed in
        ...
        """
        best_metrics = {
            'fitness': float('-inf'),
            'genome': None
        }

        run_history = []

        population = self.create_population()
        for i in range(generations):
            # print('Population at gen', i, [ind.genome for ind in population])
            self._generation+=1
            ranked = self.evaluate(population)
            fitnesses = [indF.fitness for indF in ranked]

            # ----- station‑keeping (min / mean / max) --------------------------------
            stats = {
                'min' : min(fitnesses),
                'mean': sum(fitnesses) / len(population),
                'max' : max(fitnesses)
            }
            run_history.append(stats)

            print(f"f'Generation: {self._generation}' | Fitness statistics → {stats}")
            
            #station keeping
            for indF in ranked:
                ind = population[indF.index]
                fitness = indF.fitness
                if fitness > best_metrics.get('fitness'):
                    best_metrics['fitness'] = fitness
                    best_metrics['genome'] = [gene for gene in ind.genome]

            # print('Best:', best_metrics)
            
            #next generation
            new_pop = self.crossover(population, ranked)
            self.mutate(new_pop)
            population = new_pop
        return best_metrics, run_history
            

import matplotlib.pyplot as plt


def plot_history(best_metrics, run_history=None):
    """
    Plots min / mean / max across generations.
    If ``run_history`` is omitted, uses ``self.run_history``.

    Returns the Matplotlib Figure (so you can call ``plt.show()`` later).
    """
    if run_history is None:
        run_history = run_history or []

    # ------------------------------------------------------------------
    # Prepare data
    # ------------------------------------------------------------------
    gens   = [i for i in range(len(run_history))]          # we reuse min as index (any monotonic key works)
    mins   = [h['min'] for h in run_history]
    means  = [h['mean'] for h in run_history]
    maxes  = [h['max'] for h in run_history]

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))

    colors = {'min': 'tab:red', 'mean': 'tab:orange', 'max': 'tab:green'}

    ax.plot(gens, mins,    color=colors['min'], label='Min')
    ax.plot(gens, means,   color=colors['mean'], label='Mean')
    ax.plot(gens, maxes,   color=colors['max'], label='Max')
    # ax.plot(gens, mins,   marker='o', color=colors['min'], label='Min')
    # ax.plot(gens, means,  marker='s', color=colors['mean'], label='Mean')
    # ax.plot(gens, maxes,  marker='^', color=colors['max'], label='Max')

    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness value')
    ax.set_title('Per-generation fitness statistics')
    ax.legend()
    fig.tight_layout()

    return fig


# genes = GenePool()
# print(genes.valid)
# gene = genes.random_gene(k=1)
# print("gene:", gene)
# print("phenotype:", genes.phenotype_from_gene(gene[0]))

# ind = Individual(3)
# print(ind.genome)
# print(ind.fitness())

solver = EvoSolver(500, 25, Individual, 55)
best, history = solver.evolve(500)
print('Best:', best)
fig = plot_history(best, history)
fig.savefig('results.png')

