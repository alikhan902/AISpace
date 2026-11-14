from collections import defaultdict

def solve(n):
    if n == 0:
        return {0: 1}
    if n == 1:
        return {}

    factors = defaultdict(int)
    # Trial division for small factors
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            factors[i] += 1
            n //= i
    
    # Check if n is prime or perfect power
    if n > 1:
        # Check if n is a perfect power
        for exp in range(2, 100):
            root = round(n**(1/exp))
            if root >= 2 and root**exp == n:
                factors[root] += exp
                n = 1
                break
        
        # If n is still > 1, it's prime
        if n > 1:
            factors[n] = 1

    return dict(factors)