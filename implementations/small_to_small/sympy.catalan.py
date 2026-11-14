from math import comb

def solve(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return comb(2*n, n) // (n + 1)