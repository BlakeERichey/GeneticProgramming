from topological.tpcomp.solver.genome.gene import Position, \
    Decay, Delay, \
    Sensitivity, \
    FieldOfViewCenter, FieldOfViewWidth, \
    Decision, Structural

import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int
import logging

from enum import Enum

class Chromosome:
    loci = NotImplementedError
    def __init__(self, structure, sequence=None):
        assert len(structure) == len(type(self).loci._member_names_), "Mismatching Chromosome Structure"

        if sequence is None:
            sequence = {}
            for locus, structural_gene in enumerate(structure):
                gene_type = type(self).loci._member_names_[locus]
                arity = structural_gene.allele
                gene = gene_type.value(arity)
                sequence[gene_type.name] = gene
        else:
            #check structure
            assert len(sequence) == len(structure)
            for locus, structural_gene in enumerate(structure):
                gene_type = type(self).loci._member_names_[locus]
                req_arity = structural_gene.allele
                real_arity = sequence[gene_type.name].allele
                assert req_arity == real_arity, f"Mismatch arity for {gene_type}, {req_arity} != {real_arity}"

        self.sequence = Enum(
            'Sequence',
            names=sequence
        )

    def __repr__(self):
        msg = f'{type(self).__name__}('
        msg += '\n  '.join(
            f'{key}={value}' 
            for key, value in 
            self.sequence._member_map_()
        )
        msg += '\n)'
        return msg

class ObservationChromosome(Chromosome):
    loci = Enum(
        'Locus', 
        names={
            'position':    Position,
            'decay':       Decay,
            'delay':       Delay,
            'sensitivity': Sensitivity,
        }
    )


class ActionChromosome(Chromosome):
    loci = Enum(
        'Locus', 
        names={
            'position':    Position,
            'decay':       Decay,
            'delay':       Delay,
            'sensitivity': Sensitivity,
            'field_of_view_center': FieldOfViewCenter,
            'field_of_view_width':  FieldOfViewWidth,
        }
    )


class LutChromosome(Chromosome):
    loci = Enum(
            'Locus', 
            names={
                'decision':    Decision,
            }
        )
    def __init__(self, *args, **kwargs):        
            super().__init__(*args, **kwargs)
            
            self._mask = np.array(list(
                gene.allele for gene in self.sequence['decision']
            )).nonzero()

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
            binary = bitarray(decisions.tolist())
            as_int = ba2int(binary)
            output = (as_int - 1) % arity
            logging.debug(f'LUT entry found for {decisions}: {output}')
            return output
        logging.debug(f'No LUT entry state {decisions}')

def make_mask(n_act_nodes, num_actions):
    min_true = int(np.floor(np.log2(num_actions))) + 1

    if n_act_nodes < min_true:
        raise ValueError(
            f"Cannot create a mask of length {n_act_nodes} that has at least "
            f"{min_true} True bits (needed for arity={num_actions})."
        )

    guaranteed = np.full(min_true, True)
    remaining_len = n_act_nodes - min_true
    random_filler = (
        np.random.choice([False, True], size=remaining_len)
        if remaining_len > 0 else np.array([])
    )
    mask = np.concatenate([guaranteed, random_filler])
    np.random.shuffle(mask)
    return mask.astype(bool)