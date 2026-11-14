def solve(n):
    if n == 0:
        return {"0": 1}
    if n == 1:
        return {}
    if n < 0:
        return {"-1": 1} | solve(-n)

    # Factorize positive n
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1

    return {str(k): v for k, v in factors.items()}