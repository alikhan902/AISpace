from math import factorial

def solve(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    numerator = factorial(2 * n)
    denominator = factorial(n) * factorial(n)
    catalan = numerator // denominator
    return catalan