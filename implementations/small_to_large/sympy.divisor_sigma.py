def solve(n, k=1):
    if n == 1:
        return 1

    # Step 1: Compute prime factorization of n
    factors = {}
    temp = n
    for i in range(2, int(math.isqrt(temp)) + 1):
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    # Step 2: For each prime factor p^m, compute the geometric series 1 + p + p^2 + ... + p^{m*k}
    result = 1
    for p, exp in factors.items():
        # Compute the geometric series sum: (p^(m*k + 1) - 1) / (p - 1)
        # But handle p = 1 (shouldn't happen here) and k = 0
        if k == 0:
            # For k=0, the series is just 1 (since p^0 = 1)
            term = 1
        else:
            # Compute the number of terms: m*k + 1
            num_terms = exp * k + 1
            # Compute p^(num_terms) - 1
            p_power = pow(p, num_terms)
            term = (p_power - 1) // (p - 1)
        result *= term

    return result