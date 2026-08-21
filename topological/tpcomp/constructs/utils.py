import math
def truncate(number, decimals=0):
    """Truncates a number to a specified number of decimals."""
    if decimals < 0:
        raise ValueError("Decimals must be a non-negative integer.")
    factor = 10.0**decimals
    return math.trunc(number * factor) / factor