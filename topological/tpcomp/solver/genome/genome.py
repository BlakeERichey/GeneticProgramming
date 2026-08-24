from tpcomp.solver.chromosome import ObservationChromosome, ActionChromosome, LutChromosome
from tpcomp.solver.gene import StrucuralGene

class Genome:
    def __init__(self, n_obs, n_act):
        self.sequence = {
            'actions':    {i: ActionChromosome() for i in range(n_act)},
            'observations': {i: ObservationChromosome() for i in range(n_obs)},
            'lut': LutChromosome()
        }

    @property
    def observations(self,):
        return self.sequence['observations']

    @property
    def actions(self,):
        return self.sequence['actions']

    @property
    def lut(self,):
        return self.sequence['lut']
