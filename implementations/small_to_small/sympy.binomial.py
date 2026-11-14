from math import factorial

def solve(n, k):
    if k < 0 or k > n:
        return 0
    if n == 0:
        return 1
    # Compute factorial of n and k
    n_fact = factorial(n)
    k_fact = factorial(k)
    n_k_fact = factorial(n - k)
    return n_fact // (k_fact * n_k_fact)