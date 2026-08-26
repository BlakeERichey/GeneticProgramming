import numpy as np
from functools import partial
from tpcomp.solver.genome.lut import make_mask, lookup
from tpcomp.solver.genome.organism import Gene, Haplotype, Chromosome, Genotype, Organism

from .schema import Schema
from collections import defaultdict
from enum import Enum

MIN = 0
MAX = 255

class Node:

    def __init__(self, chromosome):
        keys = set(
            'position', 
            'decay', 
            'delay', 
            'sensitivity', 
            'fov'
        )

        mapping = {}
        for gene in enumerate(chromosome):
            if gene.marker and gene.marker in keys:
                mapping.setdefault(gene.marker, gene)

        assert mapping.keys() == keys, "Chromosome missing necessary DNA" #FOV not necessary

        self.locus = Enum(
            'Locus',
            names=mapping
        )


class Topology(Organism):
    def __post_init__(self):
        super().__post_init__()

        self.obs_nodes = []
        self.act_nodes = []
        self.lut = None
        for chromosome in self.genotype.members:
            if chromosome.marker == 'observation':
                self.obs_nodes.append(Node(chromosome))
            if chromosome.marker == 'action':
                self.act_nodes.append(Node(chromosome))
            if chromosome.marker == 'lut':
                self.lut = chromosome
                