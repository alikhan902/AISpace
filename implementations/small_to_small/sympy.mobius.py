from collections import defaultdict

def solve(n):
    if n == 1:
        return 1

    factors = set()
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1

    if len(factors) == 0:
        return 1

    if len(factors) % 2 == 0:
        return 1
    else:
        return -1