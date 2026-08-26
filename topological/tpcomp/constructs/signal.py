import matplotlib.pyplot as plt
class Signal:
    def __init__(self, origin, emission_tick, stimulus=1):
        self.origin = origin # tower
        self.epicenter = self.origin.pos.copy() if origin else None #tower may move
        self.emission_tick = emission_tick
        self.stimulus = stimulus
        self._wavefront = None
            
    def radius_at(self, tick):
        dt = tick - self.emission_tick
        return max(dt, 0)
    
    def plot_wavefront(self, tick):
        radius = self.radius_at(tick)
        circle = plt.Circle(self.epicenter, radius, color='r', fill=False, lw=1, alpha=0.7)
        plt.gca().add_patch(circle)


from enum import Enum
from typing import List
from topological.tpcomp.solver.genome.organism import Gene, Haplotype, Chromosome, Genotype, Genome

Environment -> Topology -> Signals -> Organism
Organism -> Topology
Environment.stimulus -> Environment.stage -> Environment.commit
Organism.process(Stimulus) -> Stimulus -> Phenotype -> Stasis
Organism.respond(Action)
No Organism.reflection...
Phenotype -> Signals
Response -> 
A signal is a Protein
a codon is the data type clamping logic (uint8 = 8-arity codon)
stimulus→sensor protein→signaling state→gene activation→mRNA→new protein→cellular response

World : Organism -> Environment
Organism.transcribe(genome or chromosome) -> mRNA -> Topology
topology.translate(environment.stimulus) -> Proteins -> Signals
Organism.respond(proteins) -> Explicit Action -> Implicit Effect

translate : Phenotype
translate = lookup
transcribe : Phenotype
respond : Phenotype
# A Person controls the environment; the agent responds to the environment via its Phenotype.

class Tick(Genome):


class Signal(Genome):
    Position2D = Gene(low=0, high=64,  arity=2)
    Delay      = Gene(low=0, high=4,   arity=1)
    Jitter     = Delay
    Epicenter  = Position2D
    Wavefront  = Position2D

    def tick(self):
        if self.jitter == 0:
            self.wavefront = np.clip(wavefront + 1, 0, 64) 
        else:
            self.jitter = np.clip(self.jitter - 1, 0, 4)



def direction(source, dest):
    assert len(source) == len(dest)
    delta = np.array(dest) - np.array(source)
    delta = np.where(delta > 1, 2)
    delta = np.where(delta == 0, 1)
    delta = np.where(delta < 0, 0)
    signs = delta
    return signs

class Direction(Enum):
    LT = 0
    Equal = 1
    GT = 2

class FOV(Enum):
    Neither = 0
    LT = 1
    GT = 2
    Either = 3

def ignore(directions: List[Direction], fov: List[FOV]):
    """
        # Example usage:
        dest = signal.epicenter
        source = node.pos
        directions = direction(source, dest)
        ignore(directions, node.fov)

        # OR
        ignore(
            direction(
                signal.pos,
                node.pos
            ),
            node.fov
        )

    """
    assert len(directions) == len(fov)
    ignore = False
    for i in range(len(directions)):
        if ignore:
            break

        view = fov[i]
        sign = directions[i]

        if view == FOV.Neither:
            ignore = True
        if view == FOV.LT:
            ignore = sign != Direction.LT
        if view == FOV.GT:
            ignore = sign != Direction.GT
        if view == FOV.Either:
            ignore = False
    return ignore



def can_see(signal, node):
    fov = node.fov
    dest = signal.pos
    source = node.pos
    signs = direction(source, dest)
    for i, loc in enumerate(signs):
        a = fov[i]
        b = signs
        if a == 0 or a == b:
            accept = True
        if a == b == 0:




# def accept_signal(a: int, b: int):
#     signs = [None] * len(a) #-1, 0, 1
#     for each loc in a:
#         a < b
#         a = b
#         a > b

#     x < source_x  -> accept at x2 with fov in q1 or q4
#     dest - source -> sign = -1 => 