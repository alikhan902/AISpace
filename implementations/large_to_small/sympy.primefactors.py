import math

def solve(n):
    if n <= 0:
        return [abs(n)]

    factors = set()
    # Check for 2 separately
    if n % 2 == 0:
        factors.add(2)
        n //= 2

    # Check for odd factors starting from 3
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            n //= i
        i += 2

    # If n is a prime number greater than 2
    if n > 1:
        factors.add(n)

    return sorted(factors)