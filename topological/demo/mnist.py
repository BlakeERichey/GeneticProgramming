from .environments import MnistEnvironment
from .schema import Schema as genotype
from tpcomp.solver.evolution.witness import PositiveWitness
from tpcomp.solver.evolution.individual import Population
from tpcomp.solver.evolution.world import World
from tpcomp.solver.evolution.evolve import EvoSolver

population = Population(genotype, max_age=4)
population.create_population(n=64)
world = World(Topology, MnistEnvironment)
witness = PositiveWitness()
solver = EvoSolver(population, world, witness)
history = solver.evolve(100)
solver.population.save('mnist_100')