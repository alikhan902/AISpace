import math

def solve(n, k=1):
    if n == 1:
        return 1

    # Factorize n into its prime factors
    factors = {}
    temp = n
    i = 2
    while i * i <= temp:
        if temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
        else:
            i += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    # Compute the geometric series sum for each prime factor
    result = 1
    for p, m in factors.items():
        # Compute the geometric series sum: 1 + p^k + p^{2k} + ... + p^{mk}
        # Using the formula: (p^{(m+1)k} - 1) / (p^k - 1)
        if k == 0:
            # Special case for k=0: number of divisors
            result *= (m + 1)
        else:
            numerator = pow(p, (m + 1) * k) - 1
            denominator = pow(p, k) - 1
            if denominator == 0:
                # p^k == 1 => p = 1, but p is prime >= 2, so this is impossible
                result *= 1
            else:
                result *= numerator // denominator

    return result