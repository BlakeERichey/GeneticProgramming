import numpy as np
import dataclasses as dc
from typing import List, Union, Tuple, Optional, Callable

@dc.dataclass
class Symbol:
    rng = np.random.default_rng(seed=42)
    low:  int = 0
    high: int = 256

    def __post_init__(self):
        assert self.low < self.high, "low must be < high"

    def random(self):
        return self.validate(
            Symbol.rng.integers(self.low, self.high+1)
        )

    def validate(self, value):
        assert self.low <= value <= self.high, f"Assigned value must be in range [{self.low}, {self.high}]"
        return value

# class Language:
#     symbols: Symbol


# class Word:
#     language: Alphabet
    

class State:
    pass

class Register:
    pass

class Transcribe:
    """
        State Transition
    """
    pass

class Translate:
    """
        State->Output
    """
    pass

@dc.dataclass
class Automaton:
    symbols:    Symbol
    buffers:    List[Register]
    registers:  List[Register]
    transcribe: Transcribe
    translate:  Translate
