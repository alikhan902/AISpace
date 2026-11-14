def solve(n):
    if n < 3:
        return 2

    # Generate potential candidates using 6*j ± 1
    candidates = [i for i in range(3, n, 6)]

    # Check for primality of each candidate
    for i in candidates:
        is_prime = True
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            return i

    return None