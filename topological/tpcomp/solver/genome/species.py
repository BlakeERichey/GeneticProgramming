from topological.tpcomp.solver.genome.gene import StrucuralGene
from topological.tpcomp.solver.genome.chromosome import ObservationChromosome, ActionChromosome, LutChromosome

from enum import Enum

# class Parent(object):
#     __props__ = (
#         ('a', str, 'a var'),
#         ('b', int, 'b var')
#     )

#     def __init__(self):
#         self.test = 'foo'

# class AddPropsMeta(type):
#     def __init__(cls, name, bases, attrs):
#         cls.__props__ = sum((base.__props__ for base in bases), ()) + cls.__props__
#         super().__init__(name, bases, attrs)

# class Child(Parent, metaclass=AddPropsMeta):
#     __props__ = (
#         ('c', str, 'foo'),
    # )

@dc.dataclass
class StrucuralGene:
    "Inert to mutation and mutation without invalidating the species"
    allele: int = dc.field(init=True)
    StrucuralGene(name, factory, arity)
    StrucuralGene(allele, locus)

class Haplotype(type):
    """ A Gene with greater arity than 1 yet isnt a chromosome"""
    def __init__(self, *args, **kwargs):
        type(self).loci = Enum(
            'Locus',
            names={i: arg for i, arg in enumerate(args)}
        )

@dc.dataclass
class Position(Haplotype):
    def __init__(self, arity):
        
    arity: int = dc.field(init=True)
    low:  int = 0
    high: int = 256

class ObservationChromosome(Chromosome):
    loci = Enum(
        'Locus', 
        names={
            'position':    Haplotype(Position, 2),
            'decay':       Decay,
            'delay':       Delay,
            'sensitivity': Sensitivity,
        }
    )

class Species:
    """
        Structural consistency enforced amongst Species
    """
    chomosomes = Enum(
        'Chomosomes',
        names={
            'observations': ObservationChromosome,
            # 'actions': ActionChromosome,
            # 'lut': LutChromosome
        }
    )
    def __init__(self):
        ObservationChromosome.loci['position']
        Loci = name, gene
        Loci = 'position', Position ...

        # species parameters
        observable_range = 0, 255 # for RGB
        channels = 1 # for grayscale
        n = 4 # num actions
        
        loci = ObservationChromosome.loci
        StrucuralGene(loci.position,    2)
        StrucuralGene(loci.decay,       2)
        StrucuralGene(loci.delay,       2)
        StrucuralGene(loci.sensitivity, 2)

        loci = ActionChromosome.loci
        StrucuralGene(loci.position,             2)
            # StrucuralGene(loci.position.x,             2)
            # StrucuralGene(loci.position.y,             2)

        StrucuralGene(loci.decay,                2)
        StrucuralGene(loci.delay,                2)
        StrucuralGene(loci.sensitivity,          2)
        StrucuralGene(loci.fov,                  2)
            # StrucuralGene(loci.field_of_view_center, 2)
            # StrucuralGene(loci.field_of_view_width,  2)

        loci = LutChromosome.loci
        StrucuralGene(loci.actions,                  n)
        # StrucuralGene(loci.decision_low,             n)
        # StrucuralGene(loci.decision_high,            10)


species = Species(structure)
species = TopSpecies() #default
for chromosome in species:
    sequence = chromosome.set_alleles(structure)
concatenate(all_sequence) -> Genome
Genome.get_list() or Genome.get_binary()
genome = Genome(species)

loci = Enum(
        'Locus', 
        names={
            'position':
                factory = Position, arity = 2,
            'decay' - Decay - 1,
            'delay' - Delay - 1,
            'sensitivity' - Sensitivity - 1,
        }
    )

Translates to set_allele(arity), but arity = 1 for all of these
so

LutChromosome is the first to be a gene with greater arity than 1
so if greater than 1 arity, need custom set_allele method.

