import math
import functools
import collections
import operator

def solve(n):
    if n == 0:
        return {0: 1}
    if n == 1:
        return {}

    factors = collections.defaultdict(int)

    # Trial division to find small factors
    for i in range(2, int(math.isqrt(n)) + 1):
        while n % i == 0:
            factors[i] += 1
            n //= i

    # Pollard's rho algorithm for finding large factors
    def pollards_rho(n):
        if n == 1:
            return 1
        x, y, d = 2, 2, 1
        while d == 1:
            x = functools.reduce(operator.add, (x + random.randint(-100, 100) for _ in range(100)), 0)
            y = functools.reduce(operator.add, (y + random.randint(-100, 100) for _ in range(100)), 0)
            d = math.gcd(abs(x - y), n)
        return d

    # Periodic checks for prime or perfect power factors
    while n != 1:
        if is_prime(n):
            factors[n] = 1
            n = 1
        else:
            factor = pollards_rho(n)
            factors[factor] += 1
            n //= factor

    return factors