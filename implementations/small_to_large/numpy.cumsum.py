import numpy as np

def solve(a):
    return np.cumsum(a, dtype=np.int64)