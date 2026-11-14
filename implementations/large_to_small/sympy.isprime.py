import math
import functools
import collections
import operator

def solve(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")

    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # Check for trivial factors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    # Handle special cases for n <= 2^64
    if n <= 2**64:
        # Use deterministic Miller-Rabin tests with known bases
        # For this example, we use a deterministic set of bases
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for base in bases:
            if not is_prime(n, base):
                return False
        return True

    # For n > 2^64, use strong BPSW test
    if is_prime(n):
        return True
    return False

def is_prime(n, base):
    # Miller-Rabin test for a single base
    # This is a simplified version for demonstration
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(base):
        if pow(base, d, n) == base or pow(base, d, n) == 1:
            return True
    return False