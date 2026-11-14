def solve(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    # Use prime factorization for efficient computation
    def factorial_prime_factors(x):
        factors = {}
        d = 2
        while d * d <= x:
            while x % d == 0:
                factors[d] = factors.get(d, 0) + 1
                x //= d
            d += 1
        if x > 1:
            factors[x] = factors.get(x, 0) + 1
        return factors

    def binomial_prime_factors(n, k):
        # Compute prime factors of n! and k! and (n-k)!
        n_factors = factorial_prime_factors(n)
        k_factors = factorial_prime_factors(k)
        n_k_factors = factorial_prime_factors(n - k)

        # Subtract exponents for k! and (n-k)! from n!
        result = {}
        for prime in n_factors:
            exp = n_factors[prime]
            exp -= k_factors.get(prime, 0)
            exp -= n_k_factors.get(prime, 0)
            result[prime] = exp
        return result

    # Compute the binomial coefficient using prime factorization
    factors = binomial_prime_factors(n, k)
    result = 1
    for prime, exp in factors.items():
        result *= prime ** exp
    return result