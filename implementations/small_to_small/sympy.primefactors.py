def solve(n):
    if n == 1:
        return []

    factors = set()
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i

    return sorted(factors)