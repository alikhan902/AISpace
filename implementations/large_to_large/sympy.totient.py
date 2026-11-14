def solve(n):
    if n == 1:
        return 1
    # Factorize n into prime factors
    factors = {}
    temp = n
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp,  0) + 1

    # Calculate phi(n) using the formula
    phi = n
    for p in factors:
        phi = phi * (p - 1) // p
    return phi