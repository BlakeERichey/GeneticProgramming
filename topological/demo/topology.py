from tpcomp.solver.flat import Automaton, Symbol, Register
import numpy as np

def direction(source, dest):
    assert len(source) == len(dest)
    delta = np.array(dest) - np.array(source)
    delta = np.where(delta > 1, 2)
    delta = np.where(delta == 0, 1)
    delta = np.where(delta < 0, 0)
    signs = delta
    return signs

class Signal(Automaton):
    def __init__(self, genome):
        jitter     = Register(1)
        epicenter  = Register(2)
        wavefront  = Register(2)
    
    def step(self, *args):
        self.transcribe(*args)
        return self.translate()

    def transcribe(self, *args):
        if self.jitter != 0:
            self.jitter -= 1
        else:
            self.wavefront += 1

    def translate(self):
        return self.epicenter, self.wavefront

class Node(Automaton):
    def __init__(self, genome):
        self.position    = Register(2) # State(frozen=True), unchanging
        self.decay       = Register(1)
        self.delay       = Register(1) # jitter
        self.sensitivity = Register(1)
        self.fov         = Register(2)
        self.stimulus    = Register(1)

        self.signals     = Register(100000) # in range

    def transcribe(self, signals):
        np.where(
            # if any less than zero, wavefront hasnt made it there yet
            signal.wavefront - np.abs(self.position - signal.epicenter) < 0
        )