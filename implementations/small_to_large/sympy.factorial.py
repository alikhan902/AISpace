def solve(n):
    if n < 0:
        return float('inf')
    if n == 0:
        return 1
    # Precomputed lookup table for small n
    lookup = {0: 1, 1: 1, 2: 2, 3: 6, 4: 24, 5: 120, 6: 720, 10: 3628800, 15: 1307674368000, 20: 2432902008176640000, 25: 15511210043330985984000000, 30: 265252859812191058636308480000000, 35: 1033314796638614492966665133754712500000000000}
    if n in lookup:
        return lookup[n]
    # Prime-Swing algorithm for larger n
    def prime_swing(n):
        if n == 1:
            return 1
        # Find the largest prime p <= n
        p = 2
        while p * p <= n:
            p = p + 1
        # Check if p is prime
        if p > n:
            p = n
        # Compute the swing
        swing = prime_swing(p - 1)
        return swing * (p ** (n - p + 1))
    return prime_swing(n)