from collections import defaultdict

def solve(n, k=1):
    if n == 1:
        return 1

    factors = defaultdict(int)
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors[i] += 1
            n //= i
        i += 1
    if n > 1:
        factors[n] += 1

    result = 1
    for p, exp in factors.items():
        if k == 0:
            # σ₀(n) is the number of positive divisors of n
            result *= (exp + 1)
        else:
            # σ_k(n) is the sum of the k-th powers of the divisors of n
            # Compute geometric series: 1 + p + p^2 + ... + p^{exp * k}
            # Use formula: (p^{exp * k + 1} - 1) // (p - 1)
            if exp == 0:
                result = 1
            else:
                result *= (pow(p, exp * k + 1) - 1) // (pow(p, 1) - 1)
    return result