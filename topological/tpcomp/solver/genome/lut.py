import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int
import logging

def make_mask(num_actions, members):
    haplotype = members[0]
    n_act_nodes = haplotype.arity
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

def lookup(state, arity, allele):
        # arity is a structural gene, meaning immune to mutation... deferred until PoC
        _mask = np.array(allele).nonzero()
        logging.debug(f'Checking LUT for state {state}')
        state = np.array(state)
        decisions = state[_mask]
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