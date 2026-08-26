import numpy as np
import dataclasses as dc
from typing import List, Union, Tuple, Optional, Callable

@dc.dataclass
class Nucleotide:
    rng = np.random.default_rng(seed=42)
    low:  int = 0
    high: int = 256

    def __post_init__(self):
        assert self.low < self.high, "low must be < high"

    def random(self):
        return self.validate(
            Nucleotide.rng.integers(self.low, self.high+1)
        )

    def validate(self, value):
        assert self.low <= value <= self.high, f"Assigned value must be in range [{self.low}, {self.high}]"
        return value


@dc.dataclass
class Gene:
    low: int
    high: int
    arity: int
    marker: Optional[str] = None

    def random(self):
        nucleotide = Nucleotide(low=self.low, high=self.high)
        return tuple([
            nucleotide.random()
            for _ in range(self.arity)
        ])


@dc.dataclass
class Haplotype:
    arity:   int
    members: List[Gene]
    marker: Optional[str] = None

    def random(self):
        return tuple([
            tuple([member.random() for member in self.members])
            for _ in range(self.arity)
        ])

@dc.dataclass
class Chromosome:
    members: List[Union[Gene, Haplotype]]
    factory: Optional[Callable] = None
    marker: Optional[str] = None

    def random(self):
        if self.factory:
            return self.factory(self.members)

        return tuple(
            [member.random() for member in self.members]
        )
    
@dc.dataclass
class Genotype:
    members: List[List[Chromosome]]
    factory: Optional[Callable] = None
    
    def random(self):
        if self.factory:
            return self.factory(self.members)

        return tuple([
            tuple([chromosome.random() for chromosome in member])
            for member in self.members
        ])

    def validate(self, genome):
        # Tentative default to acceptance
        # Temporarily assumes the genome was crafted via a genotype rather than handcrafted
        return True

@dc.dataclass
class Organism:
    genotype: Genotype
    genome: Optional[Tuple[int]] = None
    
    def __post_init__(self):
        if self.genome is None:
            self.genome = self.genotype.random()
