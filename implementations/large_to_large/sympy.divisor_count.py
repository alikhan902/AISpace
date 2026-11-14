def solve(n):
    if n == 1:
        return 1 if not proper else 0
    # Compute the prime factorization of n
    factors = {}
    temp = n
    for i in range(2, int(n**0.5) + 1):
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    # Total number of divisors
    total_divisors = 1
    for exponent in factors.values():
        total_divisors *= (exponent + 1)

    # If modulus > 1, check if modulus divides n
    if modulus > 1:
        if n % modulus != 0:
            return 0
        # Compute the number of divisors of n//modulus
        n_div = n // modulus
        # Factorize n_div
        factors_div = {}
        temp_div = n_div
        for i in range(2, int(n_div**0.5) + 1):
            while temp_div % i == 0:
                factors_div[i] = factors_div.get(i, 0) + 1
                temp_div //= i
        if temp_div > 1:
            factors_div[temp_div] = factors_div.get(temp_div, 0) + 1
        # Total number of divisors of n_div
        total_divisors_div = 1
        for exponent in factors_div.values():
            total_divisors_div *= (exponent + 1)
        return total_divisors_div
    else:
        # modulus == 1
        if proper:
            return total_divisors - 1
        else:
            return total_divisors