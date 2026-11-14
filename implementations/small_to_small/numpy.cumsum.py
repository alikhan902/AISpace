import numpy as np

def solve(a):
    return np.cumsum(a, axis=None, dtype=np.int64)
    # The `axis=None` ensures the cumulative sum is computed along the entire array
    # The `dtype=np.int64` ensures the result is a new array with the same type as `a`