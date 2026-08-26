import numpy as np
from functools import partial
from topological.tpcomp.solver.genome.organism import Gene, Haplotype, Chromosome, Genotype

import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int
import logging

def make_mask(num_actions, members):
    haplotype = members[0]
    n_act_nodes = haplotype.arity
    min_true = int(np.floor(np.log2(num_actions))) + 1

    if n_act_nodes < min_true:
        raise ValueError(
            f"Cannot create a mask of length {n_act_nodes} that has at least "
            f"{min_true} True bits (needed for arity={num_actions})."
        )

    guaranteed = np.full(min_true, True)
    remaining_len = n_act_nodes - min_true
    random_filler = (
        np.random.choice([False, True], size=remaining_len)
        if remaining_len > 0 else np.array([])
    )
    mask = np.concatenate([guaranteed, random_filler])
    np.random.shuffle(mask)
    return mask.astype(bool)

class Schema(Genotype):
    def __init__(self, observation_space, action_space, n_nodes):
        Position2D  = Gene(low=0, high=64,  arity=2, marker='position')
        Decay       = Gene(low=0, high=4,   arity=1, marker='decay')
        Delay       = Gene(low=0, high=4,   arity=1, marker='delay')
        Sensitivity = Gene(low=1, high=4,   arity=1, marker='sensitivity')
        FieldOfView = Gene(low=0, high=3,   arity=1, marker='fov')
        Decision    = Gene(low=0, high=1,   arity=1)

        Action = Haplotype(
            arity=n_nodes,
            members=[
                Decision,
            ],
        )

        ObservationChromosome = Chromosome(
            members=[
                Position2D,
                Decay,
                Delay,
                Sensitivity,
            ],
            marker='observation'
        )

        ActionChromosome = Chromosome(
            members=[
                Position2D,
                Decay,
                Delay,
                Sensitivity,
                FieldOfView,
            ],
            marker='action'
        )

        LutChromosome = Chromosome(
            members=[Action],
            factory=partial(make_mask, action_space),
            marker='lut'
        )
        
        members = [
            [ObservationChromosome for _ in range(observation_space)], 
            [ActionChromosome      for _ in range(n_nodes)],
            [LutChromosome]
        ]
        super().__init__(members=members)
