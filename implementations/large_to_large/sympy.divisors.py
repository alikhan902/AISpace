def solve(n):
    if n == 1:
        return [1]
    divisors = []
    # Iterate up to sqrt(n)
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    divisors.sort()
    return divisors if not generator else iter(divisors)