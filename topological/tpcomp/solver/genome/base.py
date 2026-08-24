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

    def random(self):
        return tuple([
            tuple([member.random() for member in self.members])
            for _ in range(self.arity)
        ])

@dc.dataclass
class Chromosome:
    members: List[Union[Gene, Haplotype]]
    factory: Optional[Callable] = None

    def random(self):
        if self.factory:
            return self.factory(self.members)

        return tuple(
            [member.random() for member in self.members]
        )
    
@dc.dataclass
class Genotype:
    members: List[Chromosome]
    factory: Optional[Callable] = None
    
    def random(self):
        if self.factory:
            return self.factory(self.members)

        return tuple(
            [member.random() for member in self.members]
        )

@dc.dataclass
class Genome:
    genotype: Genotype
    sequence: Optional[Tuple[int]] = None
    
    def __post_init__(self):
        if self.sequence is None:
            self.sequence = self.genotype.random()
