from tpcomp.solver.gene import Position, \
    Decay, Delay, \
    Sensitivity, \
    FieldOfViewCenter, FieldOfViewWidth, \
    Decision

import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int
import logging

class Chromosome:
    sequence = {}
    def __repr__(self):
        msg = f'{type(self).__name__}('
        msg += '\n  '.join(f'{key}={value}' for key, value in self.sequence.items())
        msg += '\n)'
        return msg
            

class ObservationChromosome(Chromosome):
    def __init__(self, sequence=None):        
            if sequence is None:
                sequence = {}
                sequence.update(
                    {
                        i: gene_type.random() 
                        for i, gene_type in enumerate((
                            Position(),
                            Decay(),
                            Delay(),
                            Sensitivity(),
                            #FOV arity=0
                        ))
                    }
                )
            self.sequence = sequence

class ActionChromosome(Chromosome):
    def __init__(self, sequence=None):        
        if sequence is None:
            sequence = {}
            sequence.update(
                {
                    i: gene_type.random() 
                    for i, gene_type in enumerate((
                        Position(),
                        Decay(),
                        Delay(),
                        Sensitivity(),
                        FieldOfViewCenter(), 
                        FieldOfViewWidth(),

                        # should be resolved via arity... deferred for now
                        FieldOfViewCenter(),
                        FieldOfViewWidth()
                    ))
                }
            )
        self.sequence = sequence


class LutChromosome(Chromosome):
    def __init__(self, sequence=None):        
            if sequence is None:
                sequence = {}
                sequence.update(
                    {
                        i: gene_type.random() 
                        for i, gene_type in enumerate((
                            Decision(),
                            # should be resolved via arity... deferred for now; arity=5
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                        ))
                    }
                )
            self.sequence = sequence

            self._mask = np.array(list(sequence.values())).nonzero()

    def lookup(self, state, arity):
        # arity is a structural gene, meaning immune to mutation... deferred until PoC
        logging.debug(f'Checking LUT for state {state}')
        state = np.array(state)
        decisions = state[self._mask]
        assert arity < (2 << (len(decisions) - 1)) - 1
        # all False -> None, otherwise lookup
        if any(decisions):
            # 0000 - excluded
            # 0001 - int = 1; action = int - 1 mod arity -> action 0
            # 0010 - int = 2; action = int - 1 mod arity -> action 1
            # 0011 - int = 3; action = int - 1 mod arity -> action 2
            # 0100
            binary = bitarray(decisions.tolist())
            as_int = ba2int(binary)
            output = (as_int - 1) % arity
            logging.debug(f'LUT entry found for {decisions}: {output}')
            return output
        logging.debug(f'No LUT entry state {decisions}')
