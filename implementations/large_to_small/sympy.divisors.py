import math

def solve(n):
    divisors = []
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    if not divisors:
        return []  # This case should not occur for n > 1
    if isinstance(divisors, list):
        divisors.sort()
    else:
        divisors = list(divisors)
    return divisors if not isinstance(divisors, list) else divisors