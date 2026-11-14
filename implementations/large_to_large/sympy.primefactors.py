def solve(n):
    if n <= 0:
        n = abs(n)
    if n == 1:
        return []
    factors = []
    # Check for factor 2
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
    # Check for odd factors up to sqrt(n)
    f = 3
    while f * f <= n:
        if n % f == 0:
            factors.append(f)
            n //= f
        f += 2
    # If n is prime, add it
    if n > 1:
        factors.append(n)
    return factors