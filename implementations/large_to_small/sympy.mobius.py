import math

def solve(n):
    if n == 1:
        return 1

    factors = set()
    # Factor n into primes
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1

    if n > 1:
        factors.add(n)

    # Check if any prime factor appears with exponent >= 2
    has_square = False
    for p in factors:
        if n % p == 0:
            has_square = True
            break

    if has_square:
        return 0

    # Count distinct prime factors
    k = len(factors)
    return (-1) ** k