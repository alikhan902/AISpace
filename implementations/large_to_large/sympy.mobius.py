def solve(n):
    if n == 1:
        return 1
    # Factorize n into its prime factors
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    # Check for squared prime factors
    seen = set()
    for p in factors:
        if p in seen:
            return 0
        seen.add(p)
    # Count distinct prime factors
    k = len(seen)
    return 1 if k % 2 == 0 else -1