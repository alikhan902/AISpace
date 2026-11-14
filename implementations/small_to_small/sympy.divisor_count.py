def solve(n):
    if n < 1:
        raise ValueError("n must be a positive integer")

    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)

    return len(divisors)