def solve(n):
    if n == 1:
        return 1
    # Check for squared prime factors
    i = 2
    while i * i <= n:
        if n % (i * i) == 0:
            return 0
        i += 1
    # Count distinct prime factors
    count = 0
    i = 2
    while i * i <= n:
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        count += 1
    # Return 1 if even, -1 if odd
    return 1 if count % 2 == 0 else -1