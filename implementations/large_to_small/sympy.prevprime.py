import math

def solve(n):
    if n == 3:
        return 2
    if n == 4:
        return 3
    if n == 5:
        return 3
    if n == 6:
        return 5

    # Find the largest prime less than n
    candidate = n - 1

    # Check if candidate is prime
    if is_prime(candidate):
        return candidate

    # Decrement by 2 to check next possible prime
    candidate -= 2

    # Check if candidate is prime
    if is_prime(candidate):
        return candidate

    # Continue decrementing by 2 until a prime is found
    while candidate > 2:
        if is_prime(candidate):
            return candidate
        candidate -= 2

    return 2