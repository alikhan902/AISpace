import numpy as np

def solve(a, n=1):
    if not a:
        return []
    if n == 0:
        return a.copy()
    if n > len(a):
        return []
    # Compute the n-th discrete forward difference
    return np.diff(a, n, axis=0)