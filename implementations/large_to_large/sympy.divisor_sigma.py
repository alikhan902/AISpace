def solve(n, k=1):
    if n == 1:
        return 1

    # Factorize n into prime factors
    factors = {}
    temp = n
    for i in range(2, int(math.isqrt(temp)) + 1):
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    # Compute the product of geometric series for each prime factor
    result = 1
    for p, exp in factors.items():
        # Compute the geometric series sum: 1 + p^k + p^(2k) + ... + p^(exp*k)
        # This is (p^(exp*k + 1) - 1) / (p^k - 1) if p^k != 1, else exp + 1
        if k == 0:
            # For k=0, it's the number of divisors
            s = exp + 1
        else:
            p_k = pow(p, k)
            if p_k == 1:
                s = exp + 1
            else:
                # Using the geometric series formula
                s = (pow(p, (exp + 1) * k) - 1) // (p_k - 1)
        result *= s
    return result