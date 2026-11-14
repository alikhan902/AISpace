def solve(n):
    if n <= 0:
        raise ValueError("n must be a positive integer")

    modulus = 1
    proper = False

    if n == 1:
        if proper:
            return 0
        else:
            return 1

    # Compute prime factorization of n
    factors = {}
    temp = n
    i = 2
    while i * i <= temp:
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
        i += 1
    if temp > 1:
        factors[temp] = 1

    # Compute total number of divisors
    total_divisors = 1
    for exp in factors.values():
        total_divisors *= (exp + 1)

    # Apply modulus constraint
    if modulus > 1:
        if n % modulus != 0:
            return 0
        # Compute number of divisors of n//modulus
        n_divided = n // modulus
        divisors = 1
        for exp in factors.values():
            divisors *= (exp + 1)
        return divisors

    # Apply proper constraint
    if proper:
        return total_divisors - 1
    else:
        return total_divisors