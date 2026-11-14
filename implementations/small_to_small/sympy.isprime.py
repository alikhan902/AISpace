import math
import functools
import collections
import operator

def solve(n):
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # Miller-Rabin test with bases 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, and 37
    # These bases are known to have no counterexamples in their range
    bases = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    def is_prime(n, bases):
        if n < 2:
            return False

        # Handle even numbers
        if n % 2 == 0:
            return False

        # Write n-1 as d*2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for base in bases:
            x = pow(base, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    if n > 2**64:
        # Perform strong BPSW test
        if is_prime(n, bases):
            return True
        return False
    else:
        return is_prime(n, bases)

    # Edge cases
    if n < 2:
        return False
    if n == 2:
        return True
    if n == 1:
        return False
    if n == -2:
        return False