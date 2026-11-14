from math import gcd
from functools import reduce
from collections import defaultdict

def solve(n):
    if n == 0:
        return {0: 1}
    if n == 1:
        return {}
    if n < 0:
        n = -n
        factors = {
            -1: 1
        }
        n = abs(n)
    
    # Handle special cases
    if n == 2:
        return {2: 1}
    if n == 3:
        return {3: 1}
    if n == 5:
        return {5: 1}
    if n == 7:
        return {7: 1}
    if n == 11:
        return {11: 1}
    if n == 13:
        return {13: 1}
    if n == 17:
        return {17: 1}
    if n == 19:
        return {19: 1}
    if n == 23:
        return {23: 1}
    if n == 29:
        return {29: 1}
    if n == 31:
        return {31: 1}
    if n == 37:
        return {37: 1}
    if n == 41:
        return {41: 1}
    if n == 43:
        return {43: 1}
    if n == 47:
        return {47: 1}
    
    # Trial division for small factors
    factors = {
        2: 1
    }
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            factors[i] = 1
            while n % i == 0:
                n //= i
            if n == 1:
                break
    
    # Pollard's Rho algorithm for larger factors
    def pollards_rho(n):
        from random import randint
        from math import gcd
        if n == 1:
            return 2
        x, y, d = 2, 2, 1
        while d == 1:
            x = (x * x + 3) % n
            y = (y * y + 3) % n
            d = gcd(abs(x - y), n)
        return d

    while n > 1:
        factor = pollards_rho(n)
        if factor < n:
            factors[factor] = factors.get(factor, 0) + 1
            n //= factor
        else:
            factors[n] = factors.get(n, 0) + 1
            n = 1
    
    return factors