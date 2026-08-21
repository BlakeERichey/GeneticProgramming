from bitarray import bitarray
def int_to_jitter(value, max_val):
    return [False]*value + [True]*(max_val-value)

