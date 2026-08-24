import numpy as np
from functools import partial
from tpcomp.solver.genome.lut import make_mask, lookup
from tpcomp.solver.genome.base import Gene, Haplotype, Chromosome, Genotype, Genome

class Individual(Genome):
    def __init__(self, observation_space, action_space, n_nodes):
        Position2D          = Gene(low=0, high=64,  arity=2)
        Decay               = Gene(low=0, high=4,   arity=1)
        Delay               = Gene(low=0, high=4,   arity=1)
        Sensitivity         = Gene(low=1, high=4,   arity=1)
        FieldOfViewCenter2D = Gene(low=0, high=4,   arity=1)
        FieldOfViewWidth2D  = Gene(low=1, high=4,   arity=1)
        Decision            = Gene(low=0, high=1,   arity=1)

        FieldOfView = Haplotype(members=[
            FieldOfViewCenter2D,
            FieldOfViewWidth2D
        ])

        Action = Haplotype(members=[
            Decision for _ in range(n_nodes)
        ])

        ObservationChromosome = Chromosome([
            Position2D,
            Decay,
            Delay,
            Sensitivity,
        ])

        ActionChromosome = Chromosome([
            Position2D,
            Decay,
            Delay,
            Sensitivity,
            FieldOfView,
            FieldOfView,
        ])

        LutChromosome = Chromosome(
            members=[Action],
            factory=partial(make_mask, action_space)
        )
        
        self.genotype = Genotype([
            [ObservationChromosome for _ in range(observation_space)] + 
            [ActionChromosome      for _ in range(n_nodes)]           + 
            [LutChromosome]
        ])
