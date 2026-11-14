def solve(n):
    if n < 0 or n >  35:
        raise ValueError("n must be between 0 and 35 inclusive")
    
    # Compute binom(2n, n) = (2n)! / (n! * n!)
    def factorial(x):
        if x == 0:
            return 1
        return x * factorial(x - 1)

    binom_2n_n = factorial(2 * n) // (factorial(n) * factorial(n))

    # Divide by (n + 1) to get the Catalan number
    catalan = binom_2n_n // (n + 1)

    return catalan