from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass as dc
import numpy as np

class Gene:
    # loci <-> index: [start, stop) # inclusive, exclusive
    rng = np.random.default_rng(seed=43)

    def random(self):
        values = []
        for _ in range(self.arity):
            if type(self.low) is int:
                values.append(Gene.rng.integers(self.low, self.high))
            elif type(self.low) is float:
                values.append(Gene.rng.uniform(self.low, self.high))
            elif type(self.low) is bool:
                values.append(Gene.rng.choice([self.low, self.high]))
        return values if self.arity > 1 else values[0]

@dc
class Position(Gene):
    arity: int = 2 
    low:  int = 0
    high: int = 255

@dc
class Decay(Gene):
    arity: int = 1
    low:  int = 0
    high: int = 8

@dc
class Delay(Gene):
    arity: int = 1
    low:  int = 0
    high: int = 8

@dc
class Sensitivity(Gene):
    arity: int = 1
    low:  int = 1
    high: int = 8

@dc
class FieldOfViewCenter(Gene):
    arity: int = 1
    low:  float = 0.0
    high: float = 2 * np.pi

@dc
class FieldOfViewWidth(Gene):
    arity: int = 1
    low:  float = np.pi / 6
    high: float = np.pi

@dc
class Decision(Gene):
    arity: int = 1
    low: bool = False
    high: bool = True