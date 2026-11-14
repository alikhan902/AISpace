import math
import functools
import operator
import collections
import fractions
import operator

def solve(n):
    if n < 0:
        return complex('inf')

    if n == 0:
        return 1

    # Precomputed lookup table for n in 0..35
    lookup = [1] * (36)
    for i in range(1, 36):
        lookup[i] = lookup[i-1] * i

    # Handle small n using lookup table
    if n < 36:
        return lookup[n]

    # Handle n >= 36 using Prime-Swing algorithm
    def prime_swing(n):
        # Factor n into primes
        factors = {}
        temp = n
        i = 2
        while i * i <= temp:
            while temp % i == 0:
                factors[i] = factors.get(i, 0) + 1
                temp //= i
            i += 1
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1

        # Compute factorial using prime factors
        result = 1
        for p in factors:
            result *= p ** factors[p]
        return result

    return prime_swing(n)